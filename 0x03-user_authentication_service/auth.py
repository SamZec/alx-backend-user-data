#!/usr/bin/env python3
"""auth.py - Hash password"""
import bcrypt
from db import DB
from typing import TypeVar
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """ hash password """
    if password and type(password) == str:
        byte_password = bytes(password, 'utf-8')
        return bcrypt.hashpw(byte_password, bcrypt.gensalt())
    return None


def _generate_uuid() -> uuid4:
    """return a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """return a User object."""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """validates login"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if not password:
            return False
        byte_password = bytes(password, 'utf-8')
        if bcrypt.checkpw(byte_password, user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """returns the session ID as a string."""
        try:
            user = self._db.find_user_by(email=email)
        except (InvalidRequestError, NoResultFound) as e:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """returns the corresponding User to session_id"""
        if session_id and type(session_id) == str:
            try:
                user = self._db.find_user_by(session_id=session_id)
            except NoResultFound:
                return None
            return user
        return None

    def destroy_session(self, user_id: int) -> None:
        """destroys a session by setting to None"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return
        self._db.update_user(user.id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """get reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """update password"""
        if not reset_token:
            raise ValueError
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password)
        self._db.update_user(user.id, reset_token=None)
        return None
