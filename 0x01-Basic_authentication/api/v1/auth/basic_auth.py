#!/usr/bin/env python3
"""api/v1/auth/basic_auth.py - Basic auth"""


from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64


class BasicAuth(Auth):
    """BasicAuth"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization"""
        if (authorization_header and type(authorization_header) == str and
                authorization_header.startswith('Basic ')):
            return authorization_header.split(' ')[1]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Basic - Base64 decode"""
        try:
            d_byte = base64.b64decode(base64_authorization_header,
                                      validate=True)
            return d_byte.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns user email and password from Base64 decoded value."""
        if (decoded_base64_authorization_header and
                type(decoded_base64_authorization_header) == str and
                ':' in decoded_base64_authorization_header):
            values = decoded_base64_authorization_header.split(':', 1)
            return values[0], values[1]
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns User instance based on his email and password"""
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        user = None
        if User().count():
            user = User().search({'email': user_email})
            if not user:
                return None
        if not user or not user[0].is_valid_password(user_pwd):
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request"""
        header = self.authorization_header(request)
        extract = self.extract_base64_authorization_header(header)
        decode = self.decode_base64_authorization_header(extract)
        email, pwd = self.extract_user_credentials(decode)
        return self.user_object_from_credentials(email, pwd)
