"""
Class definition for the User Model

Classes:
    Source
"""
from src.models import db

from sqlalchemy import Column, Integer, String


class Source(db.Model):
    """
    A class to represent an external Source.

    ...

    Attributes
    ----------
    id : integer
        primary key
    name : str
        name of source
    link : string
        url to source page
    """
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    link = Column(String(200))
