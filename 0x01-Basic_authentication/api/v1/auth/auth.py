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
        method definition that returns True if the path
        is not in the list of strings included_paths:
            *Returns True if path is None
            *Returns True if excluded_paths is None or empty
            *Returns False if path is in excluded_paths
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        if path in excluded_paths:
            return False

        return True

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
