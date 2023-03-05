from main import app, db
from datetime import date, timedelta
from src.models.User import User
from src.models.Project import Project
from src.models.Logger import Logger


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User,
        create_default_users=create_default_users, 
        create_default_projects=create_default_projects,
        init_db_records=init_db_records,
        init_db=init_db)


def create_default_users():
    users = [User('fadmin', 'ladmin', '1', '1', 'admin', 'Enginer'),
            User('fadmin2', 'ladmin2', '2', '2', 'admin', 'Cleaner'),
            User('fadmin3', 'ladmin3', '3', '3', 'admin', 'Boss'),
            User('fuser', 'luser', '4', '4', 'user', 'Engineer'),
            ]
    db.session.add_all(users)
    db.session.commit()

def create_default_projects():
    projects = [Project("Project 1 test", date.today(), date.today() + timedelta(days=1)),
        Project("Project 2 test", date.today(), date.today() + timedelta(days=3)),
        Project("Project 3 test", date.today(), date.today() + timedelta(days=2))
    ]
    db.session.add_all(projects)
    db.session.commit()

def init_db_records():
    create_default_users()
    create_default_projects()
    project = db.session.query(Project).filter_by(id=1).first()
    users = db.session.query(User).all()
    project.users.extend(users[1:])

    project = db.session.query(Project).filter_by(id=2).first()
    project.users.extend(users[2:])    

    user = users[0]
    projects = db.session.query(Project).all()
    user.projects.extend(projects)
    db.session.commit()

def init_db():
    db.create_all()
    init_db_records()
