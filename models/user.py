#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    # Task 14
    def __init__(self, *args, **kwargs):
        """
        Initializes a user object and hashes the password for security.

        :param args: Positional arguments
        :param kwargs: Keyword arguments including 'password' for the user
        """
        if kwargs:
            user_pwd = kwargs.pop('password', None)
            if user_pwd:
                # Hash the password using MD5
                secure = hashlib.md5()
                secure.update(user_pwd.encode("utf-8"))
                secure_password = secure.hexdigest()
                kwargs['password'] = secure_password
        super().__init__(*args, **kwargs)
