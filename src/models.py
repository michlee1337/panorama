from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, UnicodeText, DateTime, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask_login import LoginManager, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy

from src import app, db, login
from src.helpers import get_or_create

# _____ MANY TO MANY ASSOCIATION TABLES ______

prerequisites = Table(
    'prerequisites',
    db.Model.metadata,
    Column('concept_id', Integer, ForeignKey('concepts.id')),
    Column('artifact_id', Integer, ForeignKey('artifacts.id'))
)

# _____ MANY TO MANY ASSOCIATION TABLES END ______

# _____ MODELS ______
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    email = Column(String(200))
    password_hash = Column(String(128))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # relationships
    artifacts = relationship('Artifact', backref='user', lazy='dynamic')

class Concept(db.Model):
    __tablename__ = 'concepts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    # relationships
    # NOTE: self <> self relationships in ConceptRelationship object
    artifacts = relationship('Artifact', backref='concept', lazy='dynamic')
    dependencies = relationship('Artifact', secondary='prerequisites',
        backref='prerequisites', lazy='dynamic')
    chunks = relationship('Chunk', backref='concept', lazy='dynamic')

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

    # error msgs
    UNKNOWN_TYPE_ERR = "Type {} is not recognized. Recognized types are {}."

    # _____ TABLE ATTRIBUTES _____

    id = Column(Integer, primary_key=True)
    relationship_type = Column(Integer, default=0)

    # _____ RELATIONSHIPS _____
    concept_a_id = Column(Integer, ForeignKey('concepts.id'))
    concept_b_id = Column(Integer, ForeignKey('concepts.id'))

    concept_a = relationship("Concept", foreign_keys=[concept_a_id], backref=backref("relationships_out", uselist=False))
    concept_b = relationship("Concept", foreign_keys=[concept_b_id], backref=backref("relationships_in", uselist=False))

    @classmethod
    def create(cls, concept_a, concept_b, typestr):
        try:
            rltn = get_or_create(db.session, cls,
                concept_a_id=concept_a.id,
                concept_b_id=concept_b.id,
                relationship_type=cls.getType(typestr))
            return rltn
        except:
            raise

    @classmethod
    def getType(cls, typestr):
        try:
            return cls.STR_TO_TYPE[typestr]
        except:
            recognized = [k for k in cls.STR_TO_TYPE].join(",")
            raise ValueError(UNKNOWN_TYPE_ERR.format(typestr, recognized))

    @classmethod
    def getTypestr(cls, type):
        try:
            return cls.TYPE_TO_STR[type]
        except:
            recognized = [k for k in cls.TYPE_TO_STR].join(",")
            raise ValueError(UNKNOWN_TYPE_ERR.format(type, recognized))

    # TODO: relationship type set/ get
    # TODO: methods to set/ get relationship

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
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(UnicodeText)

    # search metadata
    mediatype = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    vote_count = Column(Integer, default=0)
    vote_sum = Column(Integer, default=0)

    # relationships
    concept_id = Column(Integer, ForeignKey('concepts.id'))
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    chunks = relationship("Chunk", backref="artifact", order_by=[Chunk.position], collection_class=ordering_list('position'), lazy="dynamic")

    def __str__(self):
        return f"<id={self.id}, name={self.name}, link = {self.link}>"

    def mediatype_str(self):
        if self.type is None:
            return
        lookup = {
            1: "text",
            2: "video",
            3: "other"}
        return lookup[self.type]

    # class methods
    @classmethod
    def create(cls, input_dict):
        '''
        Creates a new artifact from a dictionary of relevant information.
        Will find or create relevant concepts and ConceptRelationship.
        All artifacts and chunks have an associated concept.
        A artifact<>chunk implies a nested concept relationship.
        A artifact<>prerequisite implies a related concept relationship.
        '''
        try:
            # check required data
            if input_dict['title'] == "" or input_dict['main_concept'] == "":
                raise ValueError("Title and Main Concept is required.")

            if input_dict.get("source_name") != None:  # .get() prevents key not found error
                source = Source(
                    name=input_dict["source_name"],
                    link=input_dict.get("source_link"))
            else:
                source = None

            # create main concept and add relationships
            main_concept = get_or_create(db.session, Concept, title=input_dict['main_concept'])
            artifact = cls(
                concept=main_concept,
                source=source,
                user=current_user,
                title=input_dict['title']
                )
            if len(input_dict.get("mediatype")) > 0:
                artifact.mediatype = int(input_dict["mediatype"])
            if len(input_dict.get("duration")) > 0:
                artifact.duration = int(input_dict["duration"])
            db.session.add(artifact)

            # create prerequisite concepts and add relationships
            for prereq in input_dict.getlist("prereqs[]"):
                prereq_concept = get_or_create(db.session, Concept, title=prereq)
                prereq_rltn = ConceptRelationship.create(prereq_concept, main_concept, "prerequisite")
                db.session.add(prereq_rltn)

            # create chunks with relationship to relevant artifact and concepts
            chunk_titles = input_dict.getlist("chunk_titles[]")
            chunk_concepts = input_dict.getlist("chunk_concepts[]")
            chunk_contents = input_dict.getlist("chunk_contents[]")

            for idx in range(len(chunk_titles)):
                if chunk_titles[idx] == "" or chunk_concepts[idx] == "":
                    break

                chunk_concept = get_or_create(db.session, Concept, title=chunk_concepts[idx])
                nested_rltn = get_or_create(db.session, ConceptRelationship,
                    concept_a_id=main_concept.id,
                    concept_b_id=chunk_concept.id,
                    relationship_type=2)  # nested relationship     # TODO: make this class method
                db.session.add(nested_rltn)

                chunk = Chunk(
                    artifact=artifact,
                    concept=chunk_concept,
                    title=chunk_titles[idx],
                    content=chunk_contents[idx])
                db.session.add(chunk)
                artifact.chunks.append(chunk)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise
        return

class Source(db.Model):  # external source
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    link = Column(String(200))

    # relationships
    artifacts = relationship("Artifact", backref="source")
