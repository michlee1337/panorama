from src.models import db
from src.models.concepts import Concept
from src.models.chunks import Chunk
from src.models.sources import Source

from sqlalchemy import Column, Integer, String, UnicodeText, ForeignKey, Table, func
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
    __tablename__ = 'artifacts'
    # _____ CLASS ATTRIBUTES _____
    # DEV: prevents saving unrecognized data into db

    DURATION_TO_STR = {
        0: 'Unknown',
        1: 'Minutes',
        2: 'Days',
        3: 'Months',
        4: 'Long'}

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
    vote_count = Column(Integer, default=0)
    vote_sum = Column(Integer, default=0)

    # relationships
    concept_id = Column(Integer, ForeignKey('concepts.id'))
    concept = relationship('Concept', backref='artifacts')
    prerequisites = relationship('Concept', secondary='artifact_prerequisites',
        backref='dependant_artifacts', lazy='dynamic')
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=True)
    source = relationship('Source', backref='artifacts')
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
            if form.mediatype.data not in self.MEDIATYPE_TO_STR.keys():  # Python3 .keys() returns set-like
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
            self.concept = get_or_create(db.session, Concept, title=form.concept.data)
            self.source = source
            self.user = current_user
            self.description = form.description.data
            self.title = form.title.data
            self.mediatype = form.mediatype.data
            self.duration = form.duration.data

            # create prerequisite concepts and add relationships
            for prereq in form.prerequisites.data:
                prereq_concept = get_or_create(db.session, Concept, title=prereq)
                self.prerequisites.append(prereq_concept)

            num_chunks = len(self.chunks.all())
            for i, chunk_entry in enumerate(form.chunks.entries):
                chunk_concept = get_or_create(db.session, Concept, title=chunk_entry.concept.data)
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

    def duration_str(self):
        return self.DURATION_TO_STR[self.duration]

    def mediatype_str(self):
        return self.MEDIATYPE_TO_STR[self.mediatype]

    @classmethod
    def search(cls, arg_dict):
        accepted_keys = {"title",
            "mediatype",
            "duration",
            "concept",
            "sub_concepts",
            "submit"}
        filters = {}

        for key, value in arg_dict.items():
            if len(value) == 0 or key == "title" or key=="sub_concepts" or key=="submit" or key == "concept":
                pass
            elif key not in accepted_keys:
                flash("Search term {} not recognized and is ignored".format(key))
            else:
                filters[key] = value

        query = Artifact.query.filter_by(**filters)

        if arg_dict.get("concept") != "":
            query = query.filter(Artifact.concept.has(Concept.title == arg_dict["concept"]))

        if arg_dict.get("sub_concepts") != "":
            subs = arg_dict["sub_concepts"].split()
            query = query.join(Chunk).join(Concept).filter(Concept.title.in_(subs))

        if arg_dict.get("title") != "":
            query = query.filter(Artifact.title.contains(arg_dict["title"]))

        artifacts = query.all()
        return artifacts

    @classmethod
    def duration_options(cls):
        return [(k, v) for k, v in cls.DURATION_TO_STR.items()]

    @classmethod
    def mediatype_options(cls):
        return [(k, v) for k, v in cls.MEDIATYPE_TO_STR.items()]
