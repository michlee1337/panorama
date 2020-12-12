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
    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    email = Column(String(200))
    password_hash = Column(String(128))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Source(db.Model):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    link = Column(String(200))

    # relationships
    resources = relationship("Resource", backref="source")
    studyplans = relationship("Studyplan", backref="source")

class Resource(db.Model):
    __tablename__ = 'resources'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    link = Column(String(500))
    depth = Column(Integer, nullable=True)
    type = Column(Integer, nullable=True)
    est_time = Column(Integer, nullable=True)
    vote_count = Column(Integer, default=0)
    vote_sum = Column(Integer, default=0)
    # instructions: filler "focus on" << should probably be a separate votable entity

    # relationships
    source_id = Column(Integer, ForeignKey('sources.id'))
    readings = relationship("Reading", backref="resource")

    def __str__(self):
        return f"<id={self.id}, name={self.name}, link = {self.link}>"

    def depth_str(self):
        lookup = {
            1: "beginner",
            2: "intermediate",
            3: "advanced"
        }
        return lookup[self.depth]

    def type_str(self):
        lookup = {
            1: "text",
            2: "video",
            3: "other"
        }
        return lookup[self.type]

class Concept(db.Model):
    __tablename__ = 'concepts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    # relationships
    resources = relationship(
        "Resource",
        secondary=lambda: concept_resources,
        backref=backref("concepts", lazy="dynamic"),
        lazy="dynamic"
    )

    # NOTE: Concepts have **two** **self** many-to-many relationships
    ## parents <> children denotes specialization
    ## prerequisites <> prerequisite_for denotes background knowledge required
    parents = relationship(
        'Concept',
        secondary=nested_concepts,
        primaryjoin=id == nested_concepts.c.child_id,
        secondaryjoin=id == nested_concepts.c.parent_id,
        backref=backref('children', lazy="dynamic"),
        lazy="dynamic"
    )

    prerequisites = relationship(
        'Concept',
        secondary=prerequisites,
        primaryjoin=id == prerequisites.c.after_id,
        secondaryjoin=id == prerequisites.c.before_id,
        backref=backref('prerequisite_for', lazy="dynamic"),  # DEV: Someone help me w names
        lazy="dynamic"
    )

class Reading(db.Model):  # workaround to use ordering_list
    __tablename__ = 'readings'
    id = Column(Integer, primary_key=True)
    description = Column(String(1000))

    # relationships
    resource_id = Column(db.Integer, ForeignKey('resources.id'))
    topic_id = Column(Integer, ForeignKey('topics.id'))
    position = Column(Integer)

    # DEV: This is temporary as future refactoring to have a less awkward divison between
    ## Studyplans and Readings will be done that allows for a search on a shared parent model.
    def getMatchingReadings(arg_dict):
        seen_keys = {}  # ensure no duplicate keys
        filter_sql = []

        for key, value in arg_dict.items():
            if key in seen_keys:
                flash("Search term duplicated. Only first instance considered.")
            elif key == "term":
                filter_sql.append("resources.{} LIKE '%%{}%%'".format("name", value))
            elif key == "depth" or key== "type":
                filter_sql.append("resources.{}={}".format(key, value))
        result = db.engine.execute("SELECT * FROM readings, resources WHERE " + " AND ".join(filter_sql))
        reading, readings = {}, []
        for row in result:
            for column, value in row.items():
                # build up the dictionary
                reading = {**reading, **{column: value}}
            readings.append(reading)
        return readings



class Topic(db.Model):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    description = Column(String(1000))

    # relationships
    concept_id = Column(Integer, ForeignKey('concepts.id'))
    concept = relationship("Concept", backref="topics")

    studyplan_id = Column(Integer, ForeignKey('studyplans.id'))
    studyplan = relationship('Studyplan')
    position = Column(Integer)

    readings = relationship("Reading", order_by=[Reading.position], collection_class=ordering_list('position'), lazy="dynamic")
    # readings = association_proxy('_readings', 'readings')

class Studyplan(db.Model):
    __tablename__ = 'studyplans'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(1000))
    # relationships
    source_id = Column(Integer, ForeignKey('sources.id'))
    concept_id = Column(Integer, ForeignKey('concepts.id'))
    concept = relationship("Concept", backref="studyplans")
    topics = relationship("Topic", order_by=[Topic.position],
                        collection_class=ordering_list('position'))

    def create(input_dict):
        '''
        Creates a new studyplan from a dictionary of relevant information.
        Will find or create relevant concepts/ resources,
        and create all newly implied relationships.

        All studyplans and topics have an associated concept.

        A studyplan<>topic implies a parent<>child concept relationship.
        A studyplan<>prerequisite implies a prerequisite_for<>prerequisite concept relationship.
        '''
        try:
            # check required data
            if input_dict['title'] == "" or input_dict['about'] == "":
                raise ValueError

            # create studyplan with relationship to about concept
            concept = get_or_create(db.session, Concept, title=input_dict['about'])
            studyplan = Studyplan(title=input_dict['title'], description=input_dict['description'], concept=concept)
            db.session.add(studyplan)

            # create prerequisite concepts and add relationships
            for prereq in input_dict['prerequisites'].split(','):
                prereq_concept = get_or_create(db.session, Concept, title=prereq)
                concept.prerequisites.append(prereq_concept)

            # create topics with relationship to relevant concept
            ## remember ordered topics/ concepts for adding relationships to readings/ resources
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

            # create readings with relationship to relevant resource
            for reading_name, reading_link, reading_description, reading_depth, reading_time, reading_type, topic_idx in zip(input_dict['reading_names'].split(','), input_dict['reading_links'].split(','), input_dict['reading_descriptions'].split(','), input_dict['reading_depths'].split(','), input_dict['reading_times'].split(','), input_dict['reading_types'].split(','), input_dict['readings_to_topic_idx'].split(',')):
                if reading_name != "" and reading_link != "":
                    topic_idx = int(topic_idx)
                    resource = get_or_create(db.session, Resource,
                        name=reading_name,
                        link=reading_link,
                        depth=int(reading_depth),
                        est_time=int(reading_time),
                        type=int(reading_type))

                    resource.concepts.append(concepts[topic_idx])

                    reading = Reading(resource=resource, description=reading_description)  # DEV: add studyplan details later
                    db.session.add(reading)
                    topics[topic_idx].readings.append(reading)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    def getMatching(term):
        return Studyplan.query.filter(Studyplan.title.contains(term)).all()
