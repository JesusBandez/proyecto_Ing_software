from werkzeug.security import generate_password_hash
from . import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(5)) 
    job = db.Column(db.String(255)) 
    status = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, role, job, status=False):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role        
        self.job = job
        self.status = status

    def __repr__(self):
        return f"<User '{self.username}'>"