""" Module for encryption / decryption """

__all__ = [
    'run_encode',
    'run_decode',
]

import base64
import os
from hashlib import scrypt, sha256

from attrs import define, field
from Crypto import Random
from Crypto.Cipher import AES


def run_encode(
        key: str,
        message: bytes
) -> base64:
    """ Encrypt key with secret phrase """

    iv = Random.new().read(AES.block_size)
    a_k_e_y = sha256(key.encode('utf-8')).digest()
    obj = AES.new(a_k_e_y, AES.MODE_CFB, iv)
    return base64.urlsafe_b64encode(obj.encrypt(message)) + b":::" + iv


def run_decode(
        key: str,
        cipher: bytes
) -> bytes:
    """ Decrypt key with secret phrase """
    a_k_e_y = sha256(key.encode('utf-8')).digest()
    cipher = cipher.split(b":::")
    obj = AES.new(a_k_e_y, AES.MODE_CFB, cipher[1])
    return obj.decrypt(base64.urlsafe_b64decode(cipher[0]))


@define
class CryptoService:
    N: int = field(default=2**14)
    r: int = field(default=8)
    p: int = field(default=1)
    KEY_LEN: int = 32
    SALT_LEN: int = 16

    def run_encode(self, key: str, message: bytes) -> bytes:
        # Derive encryption key
        salt = os.urandom(self.SALT_LEN)
        dk = scrypt(key.encode(), salt=salt, n=self.N, r=self.r, p=self.p, dklen=self.KEY_LEN)

        # AES-GCM
        cipher = AES.new(dk, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(message)

        # Format: base64(salt | nonce | tag | ciphertext)
        blob = salt + cipher.nonce + tag + ciphertext
        return base64.urlsafe_b64encode(blob)


    def run_decode(self, key: str, cipher: bytes) -> bytes:
        raw = base64.urlsafe_b64decode(cipher)

        salt = raw[:self.SALT_LEN]
        nonce = raw[self.SALT_LEN:self.SALT_LEN+16]
        tag = raw[self.SALT_LEN+16:self.SALT_LEN+16+16]
        ciphertext = raw[self.SALT_LEN+32:]

        dk = scrypt(key.encode(), salt=salt, n=self.N, r=self.r, p=self.p, dklen=self.KEY_LEN)

        aes = AES.new(dk, AES.MODE_GCM, nonce=nonce)
        return aes.decrypt_and_verify(ciphertext, tag)
