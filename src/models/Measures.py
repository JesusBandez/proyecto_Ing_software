from . import db

class Measures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dimension = db.Column(db.Integer)
    unit = db.Column(db.String(100))

    def __init__(self, dimension, unit):
        self.dimension = dimension
        self.unit = unit
        
    def __repr__(self):
        return f"{self.dimension} {self.unit}"
