"""
Class definitions for the Concept model and ConceptRelationship model

DEV: These cannot be seperated into seperate files
  due to circular dependency

Classes:
    Concept
    ConceptRelationship
"""

from src.models import db

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from src.helpers import get_or_create


class Concept(db.Model):
    """
    A class to represent an Concept

    ...

    Attributes
    ----------
    id : integer
        primary key
    title : str
        title of concept

    Methods
    -------
    related(self, exclude):
        Returns all concepts and relationship types of related concepts
    description(self, password):
        Returns a description of the concept
    infer_relationships(cls, session, artifact):
        Infers concept relationships from an artifact

    """
    __tablename__ = 'concepts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    def __repr__(self):
        return self.title

    def related(self, exclude):
        """
        Returns all concepts and relationship types of related concepts

            Parameters:
                exclude (string[]): A list of concept titles to exclude

            Returns:
                ((object, string)[]): A list of tuples of related concepts and
                    their relationship types
        """

        exclude = set(exclude)

        rels = []
        for rel in self.relationships_in:
            if rel.concept_a.title not in exclude:
                rels.append((rel.concept_a,
                             rel.directional_type(a_to_b=True)))
        for rel in self.relationships_out:
            if rel.concept_b.title not in exclude:
                rels.append((rel.concept_b,
                             rel.directional_type(a_to_b=False)))
        return rels

    def description(self):
        """
        Returns a desctiption of the given concept
        based on the description of artifacts on the concept

            Returns:
                (string): A description string of max length 75
        """

        dscptn = "No description found :("
        if self.artifacts:
            dscptn = self.artifacts[0].description
        return (dscptn[:75] + '..') if len(dscptn) > 75 else dscptn

    @classmethod
    def infer_relationships(cls, session, artifact):
        """
        Infers concept relationships based on an artifact.
        Creates prerequisite relationships between prerequisites
          and the main concept.
        Creates nested relationships between the main concept
          and chunk concepts.

            Parameters:
                session(db.session): The current database session
                artifact(object): An artifact object

            Returns:
                None
        """

        try:
            for prereq_concept in artifact.prerequisites:
                rltn = get_or_create(
                    session, ConceptRelationship,
                    concept_a_id=prereq_concept.id,
                    concept_b_id=artifact.concept.id,
                    relationship_type=ConceptRelationship.type("prerequisite"))
                session.add(rltn)
            for chunk in artifact.chunks:
                rltn = get_or_create(
                    session, ConceptRelationship,
                    concept_a_id=artifact.concept.id,
                    concept_b_id=chunk.concept.id,
                    relationship_type=ConceptRelationship.type("nested"))
                session.add(rltn)
            return
        except Exception as e:
            db.session.rollback()
            raise


class ConceptRelationship(db.Model):
    """
    A class to represent relationships between Concepts

    ...

    Attributes
    ----------
    TYPE_TO_STR: {int: string}
        mapping of ordinals to strings of relationship types
    STR_TO_TYPE: {string: int}
        mapping of strings to ordinals of relationship types
    DIRECTIONAL_TYPE {int: {bool: string}}
        mapping of ordinal relationship types to directional relationships

    id : integer
        primary key
    relationship_type : integer
        ordinal representing one of the recognized types

    Methods
    -------
    directional_type(self, a_to_b=True):
        Returns a string of directional relationship type
    type(cls, type_str):
        Converts a string type to an ordinal type
    """

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

    DIRECTIONAL_TYPE = {
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

    concept_a = relationship("Concept", foreign_keys=[concept_a_id],
                             backref=backref("relationships_out"),
                             post_update=True)
    concept_b = relationship("Concept", foreign_keys=[concept_b_id],
                             backref=backref("relationships_in"),
                             post_update=True)

    def directional_type(self, a_to_b=True):
        """
        Returns a string of directional relationship type

            Parameters:
                a_to_b (bool): If the direction is from concept_a to concept_b

            Returns:
                (string): The directional relationship type
        """
        return self.DIRECTIONAL_TYPE[self.relationship_type][a_to_b]

    @classmethod
    def type(cls, type_str):
        """
        Converts a string type to an ordinal type

            Parameters:
                type_str (string): The string of relationship type

            Returns:
                (int): The ordinal of relationship type
        """

        return cls.STR_TO_TYPE[type_str]
