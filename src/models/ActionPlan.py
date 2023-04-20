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
    
    human_talents = db.relationship('HumanTalent', backref='related_action_plan')
    supplies = db.relationship('MaterialsSupplies', backref='rel_action_plan')
    
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

    def human_talent_costs(self):
        return sum(human_talent.cost*human_talent.quantity for human_talent in self.human_talents)

    def supplies_costs(self):
        return sum(supply.cost*supply.quantity for supply in self.supplies)

    def plan_cost(self):
        return self.human_talent_costs() + self.supplies_costs()
        
        