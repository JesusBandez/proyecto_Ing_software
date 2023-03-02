from . import db
from src.models.Associations import user_project
from src.models.User import User
class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(255))
    start = db.Column(db.DateTime())
    finish = db.Column(db.DateTime())
    available = db.Column(db.Boolean)
    users = db.relationship('User', secondary=user_project, backref='projects')
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __init__(self, description, start, finish, available=True):
        self.description = description
        self.start = start
        self.finish = finish
        self.available = available
        self.manager_id = None

    def __repr__(self):
        return f"Project id: {self.id}, Description: {self.description}, Users: {self.users}"