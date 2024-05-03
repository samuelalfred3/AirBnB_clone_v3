#!/usr/bin/python3
""" holds class User"""
from models.base_model import BaseModel, Base
import hashlib
import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


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

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs.get("password", None):
            kwargs["password"] = self.hash_password(kwargs["password"])
        super().__init__(*args, **kwargs)

    @staticmethod
    def hash_password(password):
        """Hash the password to an MD5 value."""
        return hashlib.md5(password.encode()).hexdigest()

