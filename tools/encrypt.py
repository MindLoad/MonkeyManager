# -*- coding: utf-8 -*-
# Created: 06.09.2017
# Changed: 28.08.2019

"""
Module for encryption / decryption
"""

__author__ = 'MindLoad'

__all__ = [
    'run_encode',
    'run_decode',
]

import typing
import base64
from Crypto import Random
from Crypto.Cipher import AES
from hashlib import sha256


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
        cipher: typing.ByteString
) -> object:
    """ Decrypt key with secret phrase """

    a_k_e_y = sha256(key.encode('utf-8')).digest()
    cipher = cipher.split(b":::")
    obj = AES.new(a_k_e_y, AES.MODE_CFB, cipher[1])
    return obj.decrypt(base64.urlsafe_b64decode(cipher[0]))
