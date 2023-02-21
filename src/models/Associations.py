from . import db

user_project = db.Table('user_project',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
                    )