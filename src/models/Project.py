from . import db

class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(255))
    start = db.Column(db.DateTime())
    finish = db.Column(db.DateTime())

    def __init__(self, description, start, finish):
        self.description = description
        self.start = start
        self.finish = finish

    def __repr__(self):
        return f"Project id: {self.id}, Description: {self.description}."