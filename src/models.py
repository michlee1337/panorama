from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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
    concept_id = db.Column(db.Integer, db.ForeignKey('concepts.id'), nullable=False)
    # est_time = db.Column(db.Integer, nullable=True) # should these be tags?
    # vote_count = db.Column(db.Integer)
    # vote_sum = db.Column(db.Integer)
    # instructions: filler "focus on" << should probably be a separate votable entity

    def __str__(self):
        return f"<id={self.id}, name={self.name}, link = {self.link}>"

relationships = Table(
    'relationships',
    db.Model.metadata,
    db.Column('RelationshipId', db.Integer, primary_key=True),
    db.Column('ParentId', db.Integer, ForeignKey('concepts.id')),
    db.Column('ChildId', db.Integer, ForeignKey('concepts.id'))
)

class Concept(db.Model):
    __tablename__ = 'concepts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    resources = db.relationship('Resource', backref='concept')

    parents = relationship(
        'Concept',
        secondary=relationships,
        primaryjoin=id == relationships.c.ChildId,
        secondaryjoin=id == relationships.c.ParentId,
        backref=backref('children')
    )
