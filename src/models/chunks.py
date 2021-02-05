from src.models import db

from sqlalchemy import Column, Integer, String, UnicodeText, DateTime, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship, backref

class Chunk(db.Model):
    __tablename__ = 'chunks'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(UnicodeText)  # TODO: support CKeditor
    position = Column(Integer)  # ordered relationship

    # relationships
    artifact_id = Column(Integer, ForeignKey('artifacts.id'))
    concept_id = Column(Integer, ForeignKey('concepts.id'))
