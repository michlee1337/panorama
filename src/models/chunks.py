"""
Class definition for the Chunk model

Classes:
    Chunk
"""

from src.models import db
from src.models.concepts import Concept

from sqlalchemy import Column, Integer, String, UnicodeText, ForeignKey
from sqlalchemy.orm import relationship, backref

class Chunk(db.Model):
    """
    A class to represent a Chunk

    ...

    Attributes
    ----------
    id : integer
        primary key
    title : string
        title of chunk
    content: UnicodeText
        text content of chunk
    position: Integer
        position of chunk in artifact to support ordering
    """

    __tablename__ = 'chunks'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(UnicodeText)  # TODO: support CKeditor
    position = Column(Integer)  # ordered relationship

    # relationships
    artifact_id = Column(Integer, ForeignKey('artifacts.id'))
    concept_id = Column(Integer, ForeignKey('concepts.id'))
    concept = relationship('Concept', backref='chunks')
