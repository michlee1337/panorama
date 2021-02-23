from src.models import db

from sqlalchemy import Column, Integer, String

class Source(db.Model):  # external source
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    link = Column(String(200))
