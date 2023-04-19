from . import db

class HumanTalent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100))
    activity = db.Column(db.String(100))
    time = db.Column(db.Integer())
    quantity = db.Column(db.Integer())
    cost = db.Column(db.Float())
    responsible = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float())

    plan = db.Column(db.Integer, db.ForeignKey('action_plan.id'), nullable=False)

    def __init__(self, action, activity, time, quantity, cost, responsible, action_plan):
        self.action = action
        self.activity = activity
        self.time = time
        self.quantity = quantity
        self.cost = cost
        self.responsible = responsible
        self.total_amount = float(quantity)*float(cost)
        self.plan = action_plan
        

    def __repr__(self):
        return f"Human Talent Action: {self.action}, Responsible: {self.responsible}"