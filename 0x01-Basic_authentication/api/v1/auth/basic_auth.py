#!/usr/bin/env python3
"""api/v1/auth/basic_auth.py - Basic auth"""


from api.v1.auth.auth import Auth
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
