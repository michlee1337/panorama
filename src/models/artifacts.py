from src.models import db
from src.models.concepts import Concept
from src.models.concept_relationships import ConceptRelationship

from sqlalchemy import Column, Integer, String, UnicodeText, DateTime, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship, backref
from flask_login import LoginManager, UserMixin, current_user
from flask import flash

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy

from src.helpers import get_or_create

# _____ MANY TO MANY ASSOCIATION TABLES ______

artifact_prerequisites = Table(
    'artifact_prerequisites',
    db.Model.metadata,
    Column('concept_id', Integer, ForeignKey('concepts.id')),
    Column('artifact_id', Integer, ForeignKey('artifacts.id'))
)

class Chunk(db.Model):
    __tablename__ = 'chunks'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(UnicodeText)  # TODO: support CKeditor
    position = Column(Integer)  # ordered relationship

    # relationships
    artifact_id = Column(Integer, ForeignKey('artifacts.id'))
    concept_id = Column(Integer, ForeignKey('concepts.id'))

class Artifact(db.Model):
    __tablename__ = 'artifacts'
    # _____ CLASS ATTRIBUTES _____
    # DEV: prevents saving unrecognized data into db
    RECOGNIZED_MEDIATYPES = {0,1,2,3}

    RECOGNIZED_DURATIONS = {0,1,2,3}

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(UnicodeText)

    # search metadata
    mediatype = Column(Integer)
    duration = Column(Integer)
    vote_count = Column(Integer, default=0)
    vote_sum = Column(Integer, default=0)

    # relationships
    concept_id = Column(Integer, ForeignKey('concepts.id'))
    concept = relationship('Concept', backref='artifacts')
    prerequisites = relationship('Concept', secondary='artifact_prerequisites',
        backref='dependant_artifacts', lazy='dynamic')
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    chunks = relationship("Chunk", backref="artifact", order_by=[Chunk.position], collection_class=ordering_list('position'), lazy="dynamic")

    def __str__(self):
        return f"<id={self.id}, title={self.title}"

    # custom constructor
    def __init__(self, form):
        '''
        Creates a new artifact from a dictionary of relevant information.
        Will find or create relevant concepts and ConceptRelationship.
        All artifacts and chunks have an associated concept.
        A artifact<>chunk implies a nested concept relationship.
        A artifact<>prerequisite implies a related concept relationship.
        '''
        return self.save_changes(form, new=True)

    def save_changes(self, form, new=False):
        try:
            if new:
                db.session.add(self)

            # check required data
            if form.mediatype.data not in self.RECOGNIZED_MEDIATYPES:
                raise AttributeError("Mediatype is not recognized.")

            if form.duration.data not in self.RECOGNIZED_DURATIONS:
                raise AttributeError("Duration is not recognized.")

            if "name" in form.source.data:
                source = Source(
                    name=form.source.data["name"],
                    link=form.source.data["link"])
            else:
                source = None
            # create self
            main_concept = get_or_create(db.session, Concept, title=form.concept.data)
            self.concept = main_concept
            self.source = source
            self.user = current_user
            self.description = form.description.data
            self.title = form.title.data
            self.mediatype = form.mediatype.data
            self.duration = form.duration.data

            # create prerequisite concepts and add relationships
            for prereq in form.prerequisites.data:
                prereq_concept = get_or_create(db.session, Concept, title=prereq)

                # add to self
                self.prerequisites.append(prereq_concept)

                # add concept relationship
                prereq_rltn = ConceptRelationship(
                    concept_a=prereq_concept,
                    concept_b=main_concept,
                    typestr="prerequisite")
                db.session.add(prereq_rltn)

            for chunk in form.chunks.entries:
                chunk_concept = get_or_create(db.session, Concept, title=chunk.concept.data)

                nested_rltn = ConceptRelationship(concept_a=main_concept,
                    concept_b=chunk_concept,
                    typestr="nested")
                db.session.add(nested_rltn)

                chunk = Chunk(
                    artifact=self,
                    concept=chunk_concept,
                    title=chunk.title.data,
                    content=chunk.content.data)
                db.session.add(chunk)
                self.chunks.append(chunk)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    @classmethod
    def search(cls, arg_dict):
        accepted_keys = {"term", "mediatype", "duration"}
        filters = {}

        for key, value in arg_dict.items():
            if len(value) == 0 or key == "term":
                pass
            elif key not in accepted_keys:
                flash("Search term {} not recognized and is ignored".format(key))
            else:
                filters[key] = value

        if arg_dict.get("term") != "":
            artifacts = Artifact.query.filter(Artifact.title.contains(arg_dict["term"])).filter_by(**filters).all()
        else:
            artifacts = Artifact.query.filter_by(**filters).all()
        return artifacts

class Source(db.Model):  # external source
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    link = Column(String(200))

    # relationships
    artifacts = relationship("Artifact", backref="source")

    # def __str__(self):
    #     return self.name
