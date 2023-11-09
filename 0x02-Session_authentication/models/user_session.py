#!/usr/bin/env python3
"""models/user_session.py - Sessions in database"""


from models.base import Base


class UserSession(Base):
    """authentication system, based on Session ID stored in database"""
    def __init__(self, *args: list, **kwargs: dict):
        """Initializes objects"""
        super().__init__(self, *args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
