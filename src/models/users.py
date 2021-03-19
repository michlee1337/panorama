"""
Class definition for the User Model

Classes:
    User
"""

from src.models import db
from src.models.artifacts import Artifact

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """
    A class to represent a User.

    ...

    Attributes
    ----------
    id : integer
        primary key
    username : str
        displayed username
    email : string
        email address
    password_hash : string
        hashed password

    Methods
    -------
    set_password(self, password):
        Sets the password hash
    check_password(self, password):
        Verifies if a given password matches password hash
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    email = Column(String(200))
    password_hash = Column(String(128))

    def set_password(self, password):
        """
        Sets User.password_hash to the hash of the provided string

            Parameters:
                password (string): A plaintext password string

            Returns:
                None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks if the string password matches the stored password hash

            Parameters:
                password (string): A plaintext password string

            Returns:
                (bool): If the given string matches the stored password hash
        """
        return check_password_hash(self.password_hash, password)

    # relationships
    artifacts = relationship('Artifact', backref='user', lazy='dynamic')
