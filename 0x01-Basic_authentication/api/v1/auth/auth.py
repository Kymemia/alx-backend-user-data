#!/usr/bin/env python3

"""
class that manages the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    class definition that manages the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        method definition that returns False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        method definition that returns None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        method definition that returns None
        """
        return None
