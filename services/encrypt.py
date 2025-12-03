"""Encrypt/Decrypt services."""

__all__ = ["CryptoHandler"]

import base64
import os
from abc import ABC, abstractmethod
from hashlib import scrypt, sha256
from pathlib import Path

import chime
from loguru import logger

from Crypto import Random
from Crypto.Cipher import AES

logger.add(
    Path(__file__).cwd() / 'logs/errors.log',
    rotation="1 MB",
    compression="zip",
    format="<green>{time}</green> {level} <level>{message}</level>"
)


class CryptoServiceABC(ABC):
    """Crypto Service abstract class."""

    @abstractmethod
    def encrypt(key: str, message: bytes):
        """Encrypt income message."""

    @abstractmethod
    def decrypt(key, str, cipher: bytes):
        """Decrypt income message."""



class CryptoServiceV1(CryptoServiceABC):
    """Crypto Service v1. / Deprecated. Only for backward compatibility"""

    def encrypt(self, key: str, message: bytes) -> base64:
        """ Encrypt key with secret phrase """
        iv = Random.new().read(AES.block_size)
        a_k_e_y = sha256(key.encode('utf-8')).digest()
        obj = AES.new(a_k_e_y, AES.MODE_CFB, iv)
        return base64.urlsafe_b64encode(obj.encrypt(message)) + b":::" + iv

    def decrypt(self, key: str, cipher: bytes) -> bytes:
        """ Decrypt key with secret phrase """
        a_k_e_y = sha256(key.encode('utf-8')).digest()
        cipher = cipher.split(b":::")
        obj = AES.new(a_k_e_y, AES.MODE_CFB, cipher[1])
        return obj.decrypt(base64.urlsafe_b64decode(cipher[0]))


class CryptoServiceV2(CryptoServiceABC):
    """Crypto service v2."""

    N: int = 2**14
    r: int = 8
    p: int = 1
    KEY_LEN: int = 32
    SALT_LEN: int = 16

    def encrypt(self, key: str, message: bytes) -> bytes:
        # Derive encryption key
        salt = os.urandom(self.SALT_LEN)
        dk = scrypt(key.encode(), salt=salt, n=self.N, r=self.r, p=self.p, dklen=self.KEY_LEN)

        # AES-GCM
        cipher = AES.new(dk, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(message)

        # Format: base64(salt | nonce | tag | ciphertext)
        blob = salt + cipher.nonce + tag + ciphertext
        return base64.urlsafe_b64encode(blob)


    def decrypt(self, key: str, cipher: bytes) -> bytes:
        raw = base64.urlsafe_b64decode(cipher)

        salt = raw[:self.SALT_LEN]
        nonce = raw[self.SALT_LEN:self.SALT_LEN+16]
        tag = raw[self.SALT_LEN+16:self.SALT_LEN+16+16]
        ciphertext = raw[self.SALT_LEN+32:]

        dk = scrypt(key.encode(), salt=salt, n=self.N, r=self.r, p=self.p, dklen=self.KEY_LEN)

        aes = AES.new(dk, AES.MODE_GCM, nonce=nonce)
        return aes.decrypt_and_verify(ciphertext, tag)


class CryptoHandler:
    """
    Unified crypto handler. Supports multiple crypto backends (v1, v2, ...).
    Automatically:
      - Encrypt new values with v2
      - Decrypt values by detecting version
      - If a v1 value is decrypted → re-encrypts with v2 and returns (decrypted, new_cipher)
    """

    VERSION_PREFIX = {
        "v1": CryptoServiceV1(),
        "v2": CryptoServiceV2(),
    }

    DEFAULT_VERSION = "v2"
    FALLBACK_ORDER = ["v2", "v1"]         # first try v2, then v1

    @classmethod
    def encrypt(cls, key: str, message: bytes) -> bytes:
        """Always encrypt with the newest version."""
        service = cls.VERSION_PREFIX[cls.DEFAULT_VERSION]
        cipher = service.encrypt(key, message)
        return f"{cls.DEFAULT_VERSION}:{cipher.decode()}".encode()

    @classmethod
    def decrypt(cls, key: str, stored: bytes) -> tuple[bytes, bytes | None]:
        """
        Decrypt ciphertext.
        Returns: (decrypted_plaintext, new_cipher_if_reencoded_else_None)

        - Detects version by prefix.
        - If no prefix → treat as v1.
        - If decrypted via v1 → re-encrypt using v2 and return new cipher.
        """

        # 1. Detect prefix
        try:
            text = stored.decode()
            if ":" in text:
                version, cipher_raw = text.split(":", 1)
                cipher = cipher_raw.encode()
        except UnicodeDecodeError:
            # log here
            # old DB values (no prefix)
            version = "v1"
            cipher = stored

        # 2. Use correct or fallback decrypter
        service = cls.VERSION_PREFIX.get(version)

        # Try known version first
        try:
            decrypted = service.decrypt(key, cipher)
        except Exception:
            # Try fallback chain (v2 → v1)
            decrypted = None
            used_version = None
            for ver in cls.FALLBACK_ORDER:
                try:
                    svc = cls.VERSION_PREFIX[ver]
                    decrypted = svc.decrypt(key, cipher)
                    used_version = ver
                    break
                except Exception:
                    continue

            if decrypted is None:
                raise ValueError("Could not decrypt with any available crypto service")

            version = used_version

        # 3. If decrypt with old version → re-encrypt using v2
        if version == "v1":
            try:
                decrypted.decode()
            except UnicodeDecodeError:
                chime.error()
                return "error key", None

        if version != cls.DEFAULT_VERSION:
            new_cipher = cls.encrypt(key, decrypted)
            logger.warning(f"Renew password / Old cipher: {cipher.decode()}, New cipher: {new_cipher.decode()}")
            return decrypted.decode(), new_cipher

        return decrypted.decode(), None
