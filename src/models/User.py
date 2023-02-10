from . import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(5))
    status = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, role, status):
        self.username = username
        self.password = password
        self.role = role
        self.status = status

    def __repr__(self):
        return f"<User '{self.username}'>"