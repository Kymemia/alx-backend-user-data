#!/usr/bin/env python3
"""
class BasicAuth
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    class definition that inherits from Auth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        """
        method definition that returns the Base64 part
        of the header for a Basic Authentication:
            *Return None if authorization_header is None
            *Return None if authorization_header is not a string
            *Return None if authorization_header doesn’t start
            by Basic (with a space at the end)
            *Otherwise, return the value after Basic (after the space)
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        """
        method definition that returns the decoded value
        of a Base64 string, base64_authorization_header:
            *Return None if base64_authorization_header is None
            *Return None if base64_authorization_header is not a string
            *Return None if base64_authorization_header
            is not a valid Base64 - you can use try/except
            *Otherwise, return the decoded value as UTF8 string
                - you can use decode('utf-8')
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        method definition that returns the user email
        and password from the Base64 decoded value
            *Return None, None if decoded_base64_authorization_header is None
            *Return None,
                None if decoded_base64_authorization_header is not a string
            *Return None,
                None if decoded_base64_authorization_header doesn’t contain :
            *Otherwise, return the user email
            and the user password
                - these 2 values must be separated by a :
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(
                ":", 1)
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """
        method definition that returns the User instance
        based on his email and password
            *Return None if user_email is None or not a string
            *Return None if user_pwd is None or not a string
            *Return None if your database (file) doesn’t contain
                any User instance with email equal to user_email
            *Return None if user_pwd is not the password
                of the User instance found
        """
        if not isinstance(user_email, str) or user_email is None:
            return None

        if not isinstance(user_pwd, str) or user_pwd is None:
            return None

        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user
