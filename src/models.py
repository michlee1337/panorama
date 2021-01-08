from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, UnicodeText, DateTime, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy

from src import app, db, login
from src.helpers import get_or_create

# _____ MANY TO MANY ASSOCIATION TABLES ______
concept_artifacts = Table(
    'concept_artifacts',
    db.Model.metadata,
    Column('artifact_id', Integer, ForeignKey('artifacts.id')),
    Column('concept_id', Integer, ForeignKey('concepts.id'))
)

prerequisites = Table(
    'prerequisites',
    db.Model.metadata,
    Column('before_id', Integer, ForeignKey('artifacts.id')),
    Column('after_id', Integer, ForeignKey('artifacts.id'))
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

class Source(db.Model):  # external source
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    link = Column(String(200))

    # relationships
    artifacts = relationship("Artifact", backref="source")

class Concept(db.Model):
    __tablename__ = 'concepts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    # relationships
    # NOTE: self <> self relationships in ConceptRelationship object
    artifacts = relationship('Artifact', secondary='concept_artifacts',
        backref='concepts', lazy='dynamic')
    chunks = relationship('Chunk', backref='concept', lazy='dynamic')

class ConceptRelationship(db.Model):
    __tablename__ = 'concept_relationships'
    id = Column(Integer, primary_key=True)
    relationship_type = Column(Integer, default=0)

    # relationships
    concept_a_id = Column(Integer, ForeignKey('concepts.id'))
    concept_b_id = Column(Integer, ForeignKey('concepts.id'))

    concept_a = relationship('Concept', backref = 'relationships_out',
        primaryjoin = "concepts.concept_a_id == concepts.id")
    concept_b = relationship('Concept', backref = 'relationships_in',
        primaryjoin = "concepts.concept_b_id == concepts.id")

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

class Artifact(db.Model):
    __tablename__ = 'artifacts'
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(100))
    introduction = Column(UnicodeText)

    # search metadata
    mediatype = Column(Integer, nullable=True)
    depth = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    vote_count = Column(Integer, default=0)
    vote_sum = Column(Integer, default=0)

    # relationships
    prerequisites = relationship(
        'Artifact',
        secondary=prerequisites,
        primaryjoin=id == prerequisites.c.after_id,
        secondaryjoin=id == prerequisites.c.before_id,
        backref='prerequisite_for',  # DEV: Someone help me w names
        lazy="dynamic"
    )
    
    chunks = relationship("Chunk", order_by=[Chunk.position], collection_class=ordering_list('position'), lazy="dynamic")

    def __str__(self):
        return f"<id={self.id}, name={self.name}, link = {self.link}>"

    def depth_str(self):
        if self.depth is None:
            return
        lookup = {
            1: "beginner",
            2: "intermediate",
            3: "advanced"
        }
        return lookup[self.depth]

    def type_str(self):
        if self.type is None:
            return
        lookup = {
            1: "text",
            2: "video",
            3: "other"
        }
        return lookup[self.type]
