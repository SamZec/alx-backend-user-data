#!/usr/bin/env python3
"""api/v1/auth/basic_auth.py - Basic auth"""


from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization"""
        if (authorization_header and type(authorization_header) == str and
                authorization_header.startswith('Basic ')):
            return authorization_header.split(' ')[1]
        return None
