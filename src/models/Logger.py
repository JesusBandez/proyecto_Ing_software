from datetime import datetime
from . import db

class Logger(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    event = db.Column(db.String(255))
    date = db.Column(db.DateTime())
    hour = db.Column(db.DateTime())

    def __init__(self, event):
        self.event = event
        time_data = datetime.now()
        self.date = time_data.strptime(time_data.strftime(r'%Y-%m-%d'), r'%Y-%m-%d')
        self.hour = time_data.strptime(time_data.strftime(r'%H:%M:%S'), r'%H:%M:%S')

    def __repr__(self):
        return f"Evento: {self.event}, Fecha: {self.date}, Hora: {self.hour}"
        