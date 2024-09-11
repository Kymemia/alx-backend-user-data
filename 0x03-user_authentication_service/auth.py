#!/usr/bin/python3

"""
this is a method that takes in a *password* string arguments
and returns bytes
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    method definition that hashes the password using bcrypt
    and returns it as bytes
    """
    salt = bcrypt.gensalt()
    result = bcrypt.hashpw(password.encode('utf-8'), salt)
    return result
