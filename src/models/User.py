from . import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, username, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User '{self.username}'>"