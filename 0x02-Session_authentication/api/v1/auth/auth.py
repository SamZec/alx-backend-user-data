#!/usr/bin/env python3
"""api/v1/auth/auth.py - Auth class"""


import re
from os import getenv
from flask import request
from typing import List, TypeVar


class Auth:
    """manage API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        for item in excluded_paths:
            if item[:-1] in path:
                return False
        if (path in excluded_paths or (path + '/') in excluded_paths or
                path[:-1] in excluded_paths):
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if request and request.headers.get('Authorization'):
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None

    def session_cookie(self, request=None) -> str:
        """returns a cookie value from a request"""
        if request:
            cookie_name = getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
        return None
