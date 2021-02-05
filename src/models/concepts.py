from src.models import db

from sqlalchemy import Column, Integer, String, UnicodeText, DateTime, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship, backref

class Concept(db.Model):
    __tablename__ = 'concepts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    # relationships
    # NOTE: self <> self relationships in ConceptRelationship object
    chunks = relationship('Chunk', backref='concept', lazy='dynamic')

    def __repr__(self):
        return self.title
