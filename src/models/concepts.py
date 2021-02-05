from src.models import db

from sqlalchemy import Column, Integer, String

class Concept(db.Model):
    __tablename__ = 'concepts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    def __repr__(self):
        return self.title
