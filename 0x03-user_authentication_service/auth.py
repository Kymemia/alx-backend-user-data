#!/usr/bin/env python3

"""
this is a method that takes in a *password* string arguments
and returns bytes
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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
        except Exception as e:
            raise e
