#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel


class User(BaseModel):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    email = Column(String(128))
    password = Column(String(128))
    first_name = Column(String(128))
    last_name = Column(String(128))

    places = relationship("Place", back_populates='User',cascade="all, delete, delete-orphan")
