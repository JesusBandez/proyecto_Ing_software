from . import db

class MaterialsSupplies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100))
    activity = db.Column(db.String(100))
    category = db.Column(db.String(100))
    description = db.Column(db.String(100))
    quantity = db.Column(db.Integer())
    measure = db.Column(db.Integer, db.ForeignKey('measures.id'), nullable=False)
    cost = db.Column(db.Float())
    responsible = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float())

    def __init__(self, action, activity, category, description, quantity, measure, cost, responsible, amount):
        self.action = action
        self.activity = activity
        self.category = category
        self.description = description
        self.quantity = quantity
        self.measure = measure
        self.cost = cost
        self.responsible = responsible
        self.total_amount = amount
        
    def __repr__(self):
        return f"Materials Supplies Action: {self.action}, Responsible: {self.responsible}"