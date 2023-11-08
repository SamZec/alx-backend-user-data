#!/usr/bin/env python3
"""api/v1/auth/session_auth.py - Empty session"""


from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id and type(session_id) == str:
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """deletes the user session / logout"""
        if request and self.session_cookie(request):
            session_id = self.session_cookie(request)
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                del self.user_id_by_session_id[session_id]
                return True
        return False
