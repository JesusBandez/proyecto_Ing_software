from . import db

class Client(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    ci = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    birth_date = db.Column(db.DateTime(),nullable=False)
    mail = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.String(100),nullable=False)
    address = db.Column(db.String(300),nullable=False)
    cars = db.relationship('Car', backref='client', lazy=True)

    def __init__(self, ci, first_name, last_name, birth_date, mail, phone, address):
        self.ci = ci
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.mail = mail
        self.phone = phone        
        self.address = address

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"