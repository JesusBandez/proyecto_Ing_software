from . import db

class Logger(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    event = db.Column(db.String(255))
    date = db.Column(db.DateTime())
    hour = db.Column(db.DateTime())

    def __init__(self, event, date, hour):
        self.event = event
        self.date = date
        self.hour = hour

    def __repr__(self):
        return f"Evento: {self.event}, Fecha: {self.date}, Hora: {self.hour}"
        