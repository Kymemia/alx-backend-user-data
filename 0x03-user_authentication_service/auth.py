#!/usr/bin/env python3

"""
this is a method that takes in a *password* string arguments
and returns bytes
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import checkpw, hashpw


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        method definition that hashes the password using bcrypt
        and returns it as bytes
        """
        salt = bcrypt.gensalt()
        result = bcrypt.hashpw(password.encode('utf-8'), salt)
        return result

    def register_user(self, email: str, password: str) -> User:
        """
        method definition that registers a user
        after taking an email and password
        Args:
            email: user's email
            password: user's set password
        Raises:
            ValueError if a user already exists with the passed email
        Returns: a User object
        """
        try:
            user_exists = self._db.find_user_by(email=email)
            if user_exists:
                raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(
                    email=email, hashed_password=hashed_password
                    )
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        method definition that returns a boolean
        Args:
            email: user's email
            password: user's password
        Returns: If user exists, returns True. Any other case, returns False
        """
        try:
            user_exists = self._db.find_user_by(email=email)
            if user_exists:
                return checkpw(
                        password.encode('utf-8'), user_exists.hashed_password
                        )
            return False
        except NoResultFound:
            return False
