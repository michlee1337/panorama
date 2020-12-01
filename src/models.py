from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy

from src import app, db, login
from src.helpers import get_or_create

# _____ MANY TO MANY ASSOCIATION TABLES ______
concept_resources = Table(
    'concept_resources',
    db.Model.metadata,
    Column('resource_id', Integer, ForeignKey('resources.id')),
    Column('concept_id', Integer, ForeignKey('concepts.id'))
)

nested_concepts = Table(
    'nested_concepts',
    db.Model.metadata,
    Column('parent_id', Integer, ForeignKey('concepts.id')),
    Column('child_id', Integer, ForeignKey('concepts.id'))
)

prerequisites = Table(
    'prerequisites',
    db.Model.metadata,
    Column('before_id', Integer, ForeignKey('concepts.id')),
    Column('after_id', Integer, ForeignKey('concepts.id'))
)

# _____ MODELS ______
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(db.Integer, primary_key=True)
    username = Column(String(200))
    email = Column(String(200))
    password_hash = Column(String(128))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Resource(db.Model):
    __tablename__ = 'resources'
    id = Column(db.Integer, primary_key=True)
    name = Column(String(100))
    link = Column(String(500))
    depth = Column(db.Integer, nullable=True) # should these be tags?
    # description = Column(String)
    type = Column(db.Integer, nullable=True)
    # concept_id = Column(db.Integer, db.ForeignKey('concepts.id'), nullable=False)
    # est_time = Column(db.Integer, nullable=True) # should these be tags?
    # vote_count = Column(db.Integer)
    # vote_sum = Column(db.Integer)
    # instructions: filler "focus on" << should probably be a separate votable entity

    def __str__(self):
        return f"<id={self.id}, name={self.name}, link = {self.link}>"

class Concept(db.Model):
    __tablename__ = 'concepts'

    id = Column(db.Integer, primary_key=True)
    title = Column(String(100))
    resources = relationship('Resource', backref='concept')

    # relationships
    # NOTE: Concepts have _two_ self many-to-many relationships
    resources = relationship(
        "Resource",
        secondary=lambda: concept_resources,
        backref="concepts"
    )

    parents = relationship(
        'Concept',
        secondary=nested_concepts,
        primaryjoin=id == nested_concepts.c.child_id,
        secondaryjoin=id == nested_concepts.c.parent_id,
        backref=backref('children')
    )

    prerequisites = relationship(
        'Concept',
        secondary=prerequisites,
        primaryjoin=id == prerequisites.c.after_id,
        secondaryjoin=id == prerequisites.c.before_id,
        backref=backref('prerequisite_for')  # DEV: Someone help me w names
    )

class Reading(db.Model):  # workaround to use ordering_list
    __tablename__ = 'readings'
    id = Column(db.Integer, primary_key=True)
    description = Column(String(1000))

    # relationships
    topic_id = Column(db.Integer, ForeignKey('topics.id'))
    position = Column(db.Integer)
    resource_id = Column(db.Integer, ForeignKey('resources.id'))
    resource = relationship('Resource')

class Topic(db.Model):
    __tablename__ = 'topics'
    id = Column(db.Integer, primary_key=True)
    description = Column(String(1000))

    # relationships
    concept_id = Column(Integer, ForeignKey('concepts.id'))
    concept = relationship("Concept", backref="topics")

    studyplan_id = Column(db.Integer, ForeignKey('studyplans.id'))
    studyplan = relationship('Studyplan')
    position = Column(db.Integer)

    readings = relationship("Reading", order_by=[Reading.position], collection_class=ordering_list('position'))
    # readings = association_proxy('_readings', 'readings')

class Studyplan(db.Model):
    __tablename__ = 'studyplans'
    id = Column(db.Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(1000))
    # relationships
    concept_id = Column(Integer, ForeignKey('concepts.id'))
    concept = relationship("Concept", backref="studyplans")
    topics = relationship("Topic", order_by=[Topic.position],
                        collection_class=ordering_list('position'))

    def create(input_dict):
        try:
            if input_dict['title'] == "" or input_dict['about'] == "":
                raise ValueError

            concept = Concept(title=input_dict['about'])
            db.session.add(concept)

            studyplan = Studyplan(title=input_dict['title'], description=input_dict['description'], concept=concept)
            db.session.add(studyplan)

            for prereq in input_dict['prerequisites'].split(','):
                prereq_concept = get_or_create(db.session, Concept, title=prereq)
                concept.prerequisites.append(prereq_concept)

            topics = []
            concepts = []

            for topic_name, topic_description in zip(input_dict['topics'].split(','), input_dict['topic_descriptions'].split(',')):
                if topic_name != "":
                    topic_concept = get_or_create(db.session, Concept, title=topic_name)
                    concept.children.append(topic_concept)
                    concepts.append(topic_concept)  # for adding resources later

                    topic = Topic(concept=topic_concept, description=topic_description, studyplan=studyplan)
                    db.session.add(topic)
                    topics.append(topic)  # for adding readings later
                    studyplan.topics.append(topic)

            for reading_name, reading_link, reading_description, topic_idx in zip(input_dict['reading_names'].split(','), input_dict['reading_links'].split(','), input_dict['reading_descriptions'].split(','), input_dict['readings_to_topic_idx'].split(',')):
                if reading_name != "" and reading_link != "":
                    topic_idx = int(topic_idx)

                    resource = get_or_create(db.session, Resource, name=reading_name, link=reading_link)
                    resource.concepts.append(concepts[topic_idx])

                    reading = Reading(resource=resource, description=reading_description)  # DEV: add studyplan details later
                    db.session.add(reading)
                    topics[topic_idx].readings.append(reading)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise
