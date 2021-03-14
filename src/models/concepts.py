from src.models import db

from sqlalchemy import Column, Integer, String

class Concept(db.Model):
    __tablename__ = 'concepts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))

    def __repr__(self):
        return self.title

    def related(self, exclude):
        if exclude is None:
            exclude = set()

        rels = []
        print("DEBUG", self.relationships_in)
        for rel in self.relationships_in:
            if rel.concept_a.title not in exclude:
                rels.append((rel.concept_a, rel.directional_type(a_to_b=True)))
        for rel in self.relationships_out:
            if rel.concept_b.title not in exclude:
                rels.append((rel.concept_b, rel.directional_type(a_to_b=False)))
        return rels

    def description(self):
        return self.artifacts[0].description
