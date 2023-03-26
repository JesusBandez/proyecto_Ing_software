from . import db
from src.models.Associations import user_project
from src.models.User import User
class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(255))
    start = db.Column(db.DateTime())
    finish = db.Column(db.DateTime())
    available = db.Column(db.Boolean)
    car = db.Column(db.String(10), db.ForeignKey('car.license_plate', ondelete='SET NULL'), nullable=True)
    department = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    issue = db.Column(db.String(255))
    solution = db.Column(db.String(255))
    observations = db.Column(db.String(255))
    users = db.relationship('User', secondary=user_project, backref='projects')
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    amount = db.Column(db.Float())

    def __init__(self, description, start, finish,car,department,
            issue,solution,observations, manager_id,amount, available=True):
        self.description = description
        self.start = start
        self.finish = finish
        self.available = available
        self.car = car
        self.department = department
        self.issue = issue
        self.solution = solution
        self.observations = observations
        self.manager_id = manager_id
        self.amount = amount

    def __repr__(self):
        return f"Project id: {self.id}, Description: {self.description}, Users: {self.users}"