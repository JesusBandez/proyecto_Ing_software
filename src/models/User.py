from werkzeug.security import generate_password_hash
from src.models.Associations import user_project
from . import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(5)) 
    job = db.Column(db.String(255)) 
    status = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, username, password, role, job, status=False):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role        
        self.job = job
        self.status = status

    def __repr__(self):
        return f"<User '{self.username}'>"