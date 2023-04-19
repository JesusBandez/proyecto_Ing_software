from . import db

class ActionPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100))
    activity = db.Column(db.String(100))
    start_date = db.Column(db.DateTime())
    finish_date = db.Column(db.DateTime())
    hours = db.Column(db.Integer())
    responsible = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cost = db.Column(db.Float())
    project = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    

    def __init__(self, action, activity, start_date, finish_date, hours, responsible, cost, project):
        self.action = action
        self.activity = activity
        self.start_date = start_date
        self.finish_date = finish_date
        self.hours = hours
        self.responsible = responsible
        self.cost = cost
        self.project = project

    def __repr__(self):
        return f"Action Plan Action: {self.action}, Responsible: {self.responsible}"
        