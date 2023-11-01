#!/usr/bin/env python3
"""encrypt_password.py - Encrypting passwords"""


import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string."""
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
