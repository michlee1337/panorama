from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src import app, db

class Concept_Relationships(db.Model):
    __tablename__ = 'concept_relationships'
    parent = db.Column(db.Integer, db.ForeignKey('concept.id'), primary_key=True)
    child = db.Column(db.Integer, db.ForeignKey('concept.id'), primary_key=True)


class Concept(db.Model):
    __tablename__ = 'concept'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    parents = db.relationship('Concept_Relationships',backref='from', primaryjoin=id==Concept_Relationships.parent)
    children = db.relationship('Concept_Relationships',backref='to', primaryjoin=id==Concept_Relationships.child)

    def __str__(self):
        return f"<id={self.id}, title={self.title}>"
