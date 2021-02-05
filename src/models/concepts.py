from src.models import db
# from src.models.artifacts import Artifact

from sqlalchemy import Column, Integer, String, UnicodeText, DateTime, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship, backref

class Concept(db.Model):
    __tablename__ = 'concepts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    # relationships
    # NOTE: self <> self relationships in ConceptRelationship object
    # artifacts = relationship('Artifact', backref='concept', lazy='dynamic')
    chunks = relationship('Chunk', backref='concept', lazy='dynamic')
    # dependant_artifacts = relationship('Artifact', secondary='artifact_prerequisites',
    #     backref='prerequisites', lazy='dynamic')

    def __repr__(self):
        return self.title
