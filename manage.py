from main import app, db
from datetime import date,timedelta, datetime

from src.models.User import User
from src.models.Project import Project
from src.models.Client import Client 
from src.models.Car import Car
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
            User('fopera', 'lopera', '5', '5', 'opera', 'Operaciones'),
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

def create_default_clients():
    clients = [
        Client('V-27613548', 'Ramon', 'Duarte', datetime.strptime('2000-05-03', r'%Y-%m-%d'), 'rduarte@email.com', '04141123279', 'Caracas'),
        Client('V-671923', 'Juan', 'Fernandez', datetime.strptime('1965-09-12', r'%Y-%m-%d'), 'jfernan@email.com', '04243538954', 'Charallave'),
        Client('V-11156297', 'Pablo', 'Gomero', datetime.strptime('1970-12-3', r'%Y-%m-%d'), 'pablogome@email.com', '04247942584', 'Guatire'),
    ]

    db.session.add_all(clients)
    db.session.commit()

    clients = db.session.query(Client).all()
    cars = [
        Car('ATD820', 'Chevrolet', 'Sedan', 2000,'PJ12345U123456P', 'SD76216K946258D', 'blanco', 'Alineacion', clients[0].id),
        Car('PTK630', 'Toyota', 'Hatchback', 2003,'LM97845U123136K', 'LM63845U123648S', 'azul', 'Cambio de aceite', clients[0].id),
        Car('RT5031', 'Jeep', 'SUV', 2006,'GF97845U978456K', 'AR63845U123879D', 'amarillo', 'Limpieza de tapiceria', clients[1].id),
        Car('CX30EW', 'Nissan', 'Crossover', 2015,'HL9RT64897845ZF', 'PK61485G54387SA', 'amarillo', 'Croche', clients[2].id)
    ]
    db.session.add_all(cars)
    db.session.commit()

def init_db_records():
    create_default_users()
    create_default_projects()
    #create_default_clients()
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
