#!/usr/bin/env python3
"""api/v1/auth/session_exp_auth.py - Expiration?"""


from os import getenv
from datetime import timedelta, datetime
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """session expiration"""
    def __init__(self):
        """Initializes objects"""
        self.session_duration = 0
        if getenv('SESSION_DURATION') and int(getenv('SESSION_DURATION')):
            self.session_duration = int(getenv('SESSION_DURATION'))

    def create_session(self, user_id=None) -> str:
        """create session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
                              'user_id': user_id,
                              'created_at': datetime.now()
                              }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """return user ID base on session_id"""
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id).get('user_id')
        create = self.user_id_by_session_id.get(session_id).get('created_at')
        if not create:
            return None
        if create + timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return super().user_id_for_session_id(session_id).get('user_id')
