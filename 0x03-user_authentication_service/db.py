#!/usr/bin/env python3

"""DB module
"""
from user import User
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base


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
        """
        method definition that adds a user to the database
        Args:
            email: string
            hashed_password: string

        Returns:
            A User object
        """
        r = User(email=email, hashed_password=hashed_password)
        self._session.add(r)
        self._session.commit()
        return r

    def find_user_by(self, **kwargs) -> User:
        """
        method definition that returns the first row found in users table
        """
        try:
            result = self._session.query(User).filter_by(**kwargs).one()
            return result
        except NoResultFound:
            raise NoResultFound("No results found.")
        except InvalidRequestError:
            raise InvalidRequestError("Wrong query arguments passed.")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        method defintiion that takes user_id and keyword arguments,
        and returns None
        Args:
            user_id: user to be updated
            kwargs: keyword arguments based on what needs to be updated

        Raises:
            ValueError: If an argument doesn't correspond
                        to a user attribute is passed
        """
        try:
            result = self.find_user_by(id=user_id)

            for x, value in kwargs.items():
                if not hasattr(result, x):
                    raise ValueError(f"Invalid attribute: {x}")
                setattr(result, x, value)

            self._session.commit()

        except NoResultFound:
            raise NoResultFound("No result found.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid request.")
