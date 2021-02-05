from src.models import db
from src.models.concepts import Concept

from sqlalchemy import Column, Integer, String, UnicodeText, ForeignKey
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
    concept = relationship('Concept', backref='chunks')
