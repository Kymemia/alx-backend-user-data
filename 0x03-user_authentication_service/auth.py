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
import uuid


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
        except NoResultFound:
            return False

        if bcrypt.checkpw(
                password.encode('utf-8'), user_exists.hashed_password
                ):
            return True
        return False

    def _generate_uuid(self) -> str:
        """
        method definition to generate a new UUID
        Returns:
            string representation of a new UUID
        """
        result = str(uuid.uuid4())
        return result

    def create_session(self, email: str) -> str:
        """
        method definition that takes an email argument
        and returns the session ID as a string
        Returns:
            session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        method definition that takes a single session_id string argument
        and returns the corresponding User or None
        Args:
            session_id: user's session id
        Returns:
            None if the session ID is None.
            Otherwise, returns corresponding user.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
