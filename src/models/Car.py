from . import db

class Car(db.Model):
    license_plate = db.Column(db.String(10), primary_key=True)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100)) 
    year = db.Column(db.Integer)
    serial_car = db.Column(db.String(250))
    serial_engine = db.Column(db.String(250))
    color = db.Column(db.String(100))
    issue = db.Column(db.String(200))
    owner = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    associated_projects = db.relationship('Project', backref='projects')

    def __init__(self, license_plate, brand, model, year, serial_car, serial_engine, color, issue, owner):
        self.license_plate = license_plate
        self.serial_engine = serial_engine
        self.serial_car = serial_car
        self.brand = brand
        self.model = model
        self.year = year        
        self.color = color
        self.issue = issue
        self.owner = owner

    def __repr__(self):
        return f"{self.serial_car} {self.model} {self.owner}"
