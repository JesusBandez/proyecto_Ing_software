from . import db

class Department(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(300),nullable=False)
    associated_projects = db.relationship('Project', backref='associated_department')

    def __init__(self, description):
        self.description = description
    def __repr__(self):
        return f"{self.id} {self.description}"