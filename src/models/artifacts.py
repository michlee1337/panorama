"""
Class definition for the Chunk model

Classes:
    Chunk

Misc variables:
    artifact_prerequisites
"""

from src.models import db
from src.models.concepts import Concept
from src.models.chunks import Chunk
from src.models.sources import Source

from sqlalchemy import Column, Integer, String, UnicodeText, ForeignKey, \
    Table, func
from sqlalchemy.orm import relationship, backref
from flask_login import current_user
from flask import flash

from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.sql import or_

from src.helpers import get_or_create

# _____ MANY TO MANY ASSOCIATION TABLES ______

artifact_prerequisites = Table(
    'artifact_prerequisites',
    db.Model.metadata,
    Column('concept_id', Integer, ForeignKey('concepts.id')),
    Column('artifact_id', Integer, ForeignKey('artifacts.id'))
)


class Artifact(db.Model):
    """
    A class to represent an Artifact

    ...

    Attributes
    ----------
    DURATION_TO_STR: {int: string}
        mapping of ordinal to string duration values
    MEDIATYPE_TO_STR: {int: string}
        mapping of ordinal to string mediatype values
    id : integer
        primary key
    title : string
        title of artifact
    description: UnicodeText
        text description of artifact
    mediatype: Integer
        ordinal value of mediatype
    duration: Integer
        ordinal value of duration

    Methods
    ----------
    edit(self, form):
        Updates the artifact to match the form values
    duration_str(self):
        Returns the duration as a string
    mediatype_str(self):
        Returns the mediatype as a string
    search(cls, arg_dict):
        Returns all artifacts matching the arguments given
    duration_options(cls):
        Returns list of accepted durations as a tuple of
        ordinal and string values
    mediatype_options(cls):
        Returns list of accepted mediatypes as a tuple of
        ordinal and string values
    """

    __tablename__ = 'artifacts'
    # _____ CLASS ATTRIBUTES _____
    # DEV: prevents saving unrecognized data into db

    DURATION_TO_STR = {
        0: 'Unknown',
        1: 'Minutes',
        2: 'Days',
        3: 'Months'}

    MEDIATYPE_TO_STR = {
        0: 'Unknown',
        1: 'Text',
        2: 'Video',
        3: 'Other'}

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(UnicodeText)

    # search metadata
    mediatype = Column(Integer)
    duration = Column(Integer)

    # relationships
    concept_id = Column(Integer, ForeignKey('concepts.id'))
    concept = relationship('Concept', backref='artifacts')
    prerequisites = relationship('Concept', secondary='artifact_prerequisites',
                                 backref='dependant_artifacts', lazy='dynamic')
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=True)
    source = relationship('Source', backref='artifacts')
    user_id = Column(Integer, ForeignKey('users.id'))
    chunks = relationship("Chunk", backref="artifact",
                          order_by=[Chunk.position],
                          collection_class=ordering_list('position'),
                          lazy="dynamic")

    def __str__(self):
        return f"<id={self.id}, title={self.title}"

    # custom constructor
    def __init__(self, form):
        return self.__save_changes(form, new=True)

    def __save_changes(self, form, new=False):
        try:
            if new:
                db.session.add(self)

            # check required data
            # DEV: Python3 .keys() returns set-like
            if form.mediatype.data not in self.MEDIATYPE_TO_STR.keys():
                raise AttributeError("Mediatype is not recognized.")

            if form.duration.data not in self.DURATION_TO_STR.keys():
                raise AttributeError("Duration is not recognized.")

            if form.source.data["name"] != "":
                source = get_or_create(db.session, Source,
                                       name=form.source.data["name"],
                                       link=form.source.data["link"])

            else:
                source = None

            # create self
            self.concept = get_or_create(db.session, Concept,
                                         title=form.concept.data)
            self.source = source
            self.user = current_user
            self.description = form.description.data
            self.title = form.title.data
            self.mediatype = form.mediatype.data
            self.duration = form.duration.data

            # create prerequisite concepts and add relationships
            for prereq in form.prerequisites.data:
                prereq_concept = get_or_create(db.session, Concept,
                                               title=prereq)
                self.prerequisites.append(prereq_concept)

            # create chunks
            num_chunks = len(self.chunks.all())
            for i, chunk_entry in enumerate(form.chunks.entries):
                chunk_concept = get_or_create(db.session, Concept,
                                              title=chunk_entry.concept.data)
                if i < num_chunks:
                    chunk = self.chunks[i]
                    chunk.concept = chunk_concept
                    chunk.title = chunk_entry.title.data
                    chunk.content = chunk_entry.content.data
                else:
                    chunk = Chunk(
                        artifact=self,
                        concept=chunk_concept,
                        title=chunk_entry.title.data,
                        content=chunk_entry.content.data)
                    self.chunks.append(chunk)
                db.session.add(chunk)

            for i in range(len(form.chunks.entries)-1, num_chunks-1):
                db.session.delete(self.chunks[-1])

            # infer concept relationships from artifact
            Concept.infer_relationships(db.session, self)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    def edit(self, form):
        """
        Updates the artifact to match the form values

            Parameters:
                form (werkzeug.MultiDict): A mapping of attributes to values

            Returns:
                None
        """
        return self.__save_changes(form, new=False)

    def duration_str(self):
        """
        Returns the duration as a string

            Parameters:
                None

            Returns:
                (string): the duration value
        """
        return self.DURATION_TO_STR[self.duration]

    def mediatype_str(self):
        """
        Returns the mediatype as a string

            Parameters:
                None

            Returns:
                (string): the mediatype value
        """
        return self.MEDIATYPE_TO_STR[self.mediatype]

    @classmethod
    def search(cls, arg_dict):
        """
        Returns all artifacts matching the arguments given

            Parameters:
                arg_dict({string: string}): a mapping of attribute key to value

            Returns:
                (Artifact[]): a list of atrifacts matching the arguments
        """
        accepted_keys = {"title",
                         "mediatype",
                         "duration",
                         "concept",
                         "sub_concepts",
                         "source",
                         "submit"}
        special_filters = {"title",
                           "sub_concepts",
                           "concept",
                           "source"}

        filters = {}

        for key, value in arg_dict.items():
            if len(value) == 0 or key == "search" or key in special_filters:
                pass
            elif key not in accepted_keys:
                flash("Term {} not recognized and is ignored".format(key))
            else:
                filters[key] = value

        query = Artifact.query.filter_by(**filters)

        if arg_dict.get("concept") != "":
            query = query.filter(Artifact.concept.has(
                Concept.title == arg_dict["concept"]))

        if arg_dict.get("sub_concepts") != "":
            subs = arg_dict["sub_concepts"].split()
            query = query.join(Chunk).join(Concept).filter(
                Concept.title.in_(subs))

        if arg_dict.get("source") != "":
            query = query.filter(Artifact.source.has(
                Source.name == arg_dict["source"]))

        if arg_dict.get("title") != "":
            query = query.filter(Artifact.title.contains(arg_dict["title"]))

        artifacts = query.all()
        return artifacts

    @classmethod
    def duration_options(cls):
        """
        Returns list of accepted durations as a tuple of
        ordinal and string values

            Parameters:
                None

            Returns:
                ((int, string))[]: List of accepted durations
        """

        return [(k, v) for k, v in cls.DURATION_TO_STR.items()]

    @classmethod
    def mediatype_options(cls):
        """
        Returns list of accepted mediatypes as a tuple of
        ordinal and string values

            Parameters:
                None

            Returns:
                ((int, string))[]: List of accepted mediatypes
        """
        return [(k, v) for k, v in cls.MEDIATYPE_TO_STR.items()]
