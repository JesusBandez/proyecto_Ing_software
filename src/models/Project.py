from . import db
from src.models.Associations import user_project
from src.models.User import User
class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(255))
    start = db.Column(db.DateTime())
    finish = db.Column(db.DateTime())
    available = db.Column(db.Boolean)
    issue = db.Column(db.String(255))
    solution = db.Column(db.String(255))
    observations = db.Column(db.String(255))
    users = db.relationship('User', secondary=user_project, backref='projects')
    amount = db.Column(db.Float())

    car = db.Column(db.String(10), db.ForeignKey('car.license_plate'), nullable=True)
    department = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    action_plans = db.relationship('ActionPlan', backref='associated_project')

    def __init__(self, description, start, finish, car, department,
            issue,solution,observations, manager_id, available=True):
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


    def __repr__(self):
        return f"Project id: {self.id}, Description: {self.description}, Users: {self.users}"

    def project_cost(self):
        return sum(plan.plan_cost() for plan in self.action_plans)