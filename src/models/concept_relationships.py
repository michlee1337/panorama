from src.models import db
from src.models.artifacts import Concept

from sqlalchemy import Column, Integer, String, UnicodeText, DateTime, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship, backref

class ConceptRelationship(db.Model):
    __tablename__ = 'concept_relationships'
    # _____ CLASS ATTRIBUTES _____
    # DEV: encapsulating conversion
    TYPE_TO_STR = {
        0: "undetermined",
        1: "prerequisite",
        2: "nested"
    }

    STR_TO_TYPE = {
        "undetermined": 0,
        "prerequisite": 1,
        "nested": 2
    }

    # _____ TABLE ATTRIBUTES _____

    id = Column(Integer, primary_key=True)
    relationship_type = Column(Integer, default=0)

    # _____ RELATIONSHIPS _____
    concept_a_id = Column(Integer, ForeignKey('concepts.id'))
    concept_b_id = Column(Integer, ForeignKey('concepts.id'))

    concept_a = relationship("Concept", foreign_keys=[concept_a_id], backref=backref("relationships_out", uselist=False))
    concept_b = relationship("Concept", foreign_keys=[concept_b_id], backref=backref("relationships_in", uselist=False))

    def __init__(self, concept_a, concept_b, typestr):
        try:
            self.concept_a_id = concept_a.id
            self.concept_b_id = concept_b.id
            self.relationship_type = self.STR_TO_TYPE[typestr]
        except:
            raise
