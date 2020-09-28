from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src import app, db

# class Resource(db.Model):
#     __tablename__ = 'resources'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     link = db.Column(db.String(500))

class Concept_Relationships(db.Model):
    __tablename__ = 'concept_relationships'
    parent_id = db.Column(db.Integer, db.ForeignKey('concepts.id'), primary_key=True)
    child_id= db.Column(db.Integer, db.ForeignKey('concepts.id'), primary_key=True)
    # NOTE: to add a relationship: Concept_Relationships(parent_concept=c1 , child_concept=c2)
    
class Concept(db.Model):
    __tablename__ = 'concepts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    # resources = db.relationship('Resource', backref='concept+', primaryjoin=id==Concept_Relationships.child)
    parents = db.relationship('Concept_Relationships', backref='parent_concept', primaryjoin=id==Concept_Relationships.child_id)  # self has parents if it is listed as a child
    children = db.relationship('Concept_Relationships', backref='child_concept', primaryjoin=id==Concept_Relationships.parent_id)

    def __str__(self):
        return f"<id={self.id}, title={self.title}, parents = {self.parents}, children = {self.children}>"
