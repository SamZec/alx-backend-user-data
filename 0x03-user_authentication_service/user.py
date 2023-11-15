#!/usr/bin/env python3
"""user.py - User model"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column


Base = declarative_base()


class User(Base):
    """users object"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __str__(self):
        """string represntation of user"""
        return f'{self.id} {self.email}'
