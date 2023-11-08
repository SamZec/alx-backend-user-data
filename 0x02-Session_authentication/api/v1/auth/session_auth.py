#!/usr/bin/env python3
"""api/v1/auth/session_auth.py - Empty session"""


from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """new authentication mechanism"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create session"""
        if user_id and type(user_id) == str:
            id = str(uuid4())
            self.user_id_by_session_id[id] = user_id
            return id
        return None
