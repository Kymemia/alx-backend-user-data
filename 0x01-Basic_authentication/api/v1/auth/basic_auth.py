#!/usr/bin/env python3
"""
class BasicAuth
"""
from api.v1.auth.auth import Auth


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
