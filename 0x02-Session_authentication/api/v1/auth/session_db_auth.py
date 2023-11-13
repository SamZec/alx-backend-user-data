#!/usr/bin/env python3
"""api/v1/auth/session_db_auth.py - Sessions in database authentication"""


from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models.user import User
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Sessions in database authentication"""
    def create_session(self, user_id=None) -> str:
        """creates and stores UserSession and returns the Session ID"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {'user_id': user_id, 'session_id': session_id}
        user_session = UserSession(**session_dict)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """returns the User ID by requesting UserSession
        in the database based on session_id
        """
        if not session_id and type(session_id) is not str:
            return None
        try:
            user_session = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if not user_session:
            return None
        if self.session_duration <= 0:
            return user_session[0].user_id
        if not user_session[0].to_json().get('created_at'):
            return None
        create = user_session[0].created_at
        if (create + timedelta(seconds=self.session_duration) <
                datetime.utcnow()):
            return None
        return user_session[0].user_id

    def destroy_session(self, request=None) -> bool:
        """destroys the UserSession based on the Session ID
        from the request cookie
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        if not user:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if not user_session[0]:
            return False
        user_session[0].remove()
        return True
