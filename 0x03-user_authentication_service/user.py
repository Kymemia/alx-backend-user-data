#!/usr/bin/env python3

"""
this is an SQLAlchemy model named, User,
for the database table, user.

Attributes:
        *id
        *email
        *hashed_password
        *session_id
        *reset_token
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String

Base = declarative_base()


class User(Base):
    """
    this will be the class definition for our user model
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """
        method definition that'll display key attributes
        """
        return (
                f"<User: {self.id} {self.email} {self.hashed_password} "
                f"{self.session_id} {self.reset_token}>"
                )
