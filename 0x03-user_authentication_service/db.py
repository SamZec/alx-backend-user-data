#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import TypeVar

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """save user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """returns the first row found in users table filtered by **kwargs"""
        session = self._session
        # user = session.query(User).filter_by(**kwargs).first()
        for item in kwargs.keys():
            if not hasattr(User, item):
                raise InvalidRequestError
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """update user’s attributes passed as arguments"""
        try:
            user = self.find_user_by(id=user_id)
        except (InvalidRequestError, NoResultFound) as e:
            raise ValueError
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError
            setattr(user, key, value)
        session = self._session
        session.add(user)
        session.commit()
        return None
