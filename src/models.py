from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy

from src import app, db, login

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password_hash = db.Column(db.String(128))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    link = db.Column(db.String(500))
    depth = db.Column(db.Integer, nullable=True) # should these be tags?
    # description = db.Column(db.String)
    type = db.Column(db.Integer, nullable=True)
    # concept_id = db.Column(db.Integer, db.ForeignKey('concepts.id'), nullable=False)
    # est_time = db.Column(db.Integer, nullable=True) # should these be tags?
    # vote_count = db.Column(db.Integer)
    # vote_sum = db.Column(db.Integer)
    # instructions: filler "focus on" << should probably be a separate votable entity

    def __str__(self):
        return f"<id={self.id}, name={self.name}, link = {self.link}>"

# relationships = Table(
#     'relationships',
#     db.Model.metadata,
#     db.Column('RelationshipId', db.Integer, primary_key=True),
#     db.Column('ParentId', db.Integer, ForeignKey('concepts.id')),
#     db.Column('ChildId', db.Integer, ForeignKey('concepts.id'))
# )

class Concept(db.Model):
    __tablename__ = 'concepts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    resources = db.relationship('Resource', backref='concept')

    # relationships
    resources = relationship("Resource",
                secondary=lambda: conept_resources,
                backref="concepts")


class Reading(db.Model):  # workaround to use ordering_list
    __tablename__ = 'studyplan_resources'
    id = db.Column(db.Integer, primary_key=True)

    # relationships
    topic_id = db.Column(db.Integer, ForeignKey('topics.id'))
    position = db.Column(db.Integer)
    resource_id = db.Column(db.Integer, ForeignKey('resources.id'))
    resource = db.relationship('Resource')

class Topic(db.Model):
    __tablename__ = 'topics'
    id = Column(db.Integer, primary_key=True)

    # relationships
    concept_id = Column(Integer, ForeignKey('concepts.id'))
    concept = relationship("Concept", backref="topics")

    studyplan_id = db.Column(db.Integer, ForeignKey('studyplans.id'))
    position = db.Column(db.Integer)

    _readings = db.relationship("Reading", order_by=[Reading.position], collection_class=ordering_list('position'))
    readings = association_proxy('_readings', 'readings')



class StudyPlan(db.Model):
    __tablename__ = 'studyplans'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    # relationships
    # concept_id = Column(Integer, ForeignKey('concepts.id'))
    # concept = relationship("Concept", backref="studyplans")  # NOTE: Studyplan <> Concept has *TWO* relationships
    prerequisite_concepts = relationship("Concept",
                secondary=lambda: prerequisites,
                backref="prereq_for")  # DEV: this needs a better name

    topics = db.relationship("Topic", order_by=[Topic.position],
                        collection_class=ordering_list('position'))

conept_resources = Table(
    'conept_resources',
    db.Model.metadata,
    Column('resource_id', Integer, ForeignKey('resources.id')),
    Column('concept_id', Integer, ForeignKey('concepts.id'))
)

prerequisites = Table(
    'prerequisites',
    db.Model.metadata,
    Column('studyplan_id', Integer, ForeignKey('studyplans.id')),
    Column('concept_id', Integer, ForeignKey('concepts.id'))
)
