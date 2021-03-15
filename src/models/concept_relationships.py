from src.models import db
from src.models.artifacts import Concept

from sqlalchemy import Column, Integer, ForeignKey
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

    DIRECTIONAL_TYPE =  {
        0: {True: "undetermined", False: "undetermined"},
        1: {True: "first", False: "second"},
        2: {True: "up", False: "down"}
    }

    # _____ TABLE ATTRIBUTES _____

    id = Column(Integer, primary_key=True)
    relationship_type = Column(Integer, default=0)

    # _____ RELATIONSHIPS _____
    concept_a_id = Column(Integer, ForeignKey('concepts.id'))
    concept_b_id = Column(Integer, ForeignKey('concepts.id'))

    concept_a = relationship("Concept", foreign_keys=[concept_a_id], backref=backref("relationships_out"))
    concept_b = relationship("Concept", foreign_keys=[concept_b_id], backref=backref("relationships_in"))

    def directional_type(self, a_to_b=True):
        return self.DIRECTIONAL_TYPE[self.relationship_type][a_to_b]

    @classmethod
    def type(cls, type_str):
        return cls.STR_TO_TYPE[type_str]
