from main import app, db
from datetime import date,timedelta, datetime

from src.models.User import User
from src.models.Project import Project
from src.models.Client import Client 
from src.models.Car import Car
from src.models.Logger import Logger
from src.models.Department import Department
from src.models.Measures import Measures
from src.models.ActionPlan import ActionPlan
from src.models.HumanTalent import HumanTalent
from src.models.MaterialsSupplies import MaterialsSupplies




@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User,
        create_default_users=create_default_users, 
        create_default_projects=create_default_projects,
        init_db_records=init_db_records,
        init_db=init_db)

def create_action_plans():
    a = ActionPlan('1', '1', date.today(), date.today(), 2, 1, 20)

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
    CARS = db.session.query(Car).all()
    DEPARTMENTS = db.session.query(Department).all()
    USERS = db.session.query(User).all()
    projects = [
        Project("Alineacion de vehiculo", date.today(), date.today() + timedelta(days=1), CARS[0].license_plate, DEPARTMENTS[2].id,
        'Necesita alineacion', 'Hay que alinearlo', 'Golpe en el capo', USERS[0].id, 30.0),
        Project("Rellenado de carroceria", date.today(), date.today() + timedelta(days=1), CARS[1].license_plate, DEPARTMENTS[1].id,
        'Raya en el capo', 'Aplicacion de masilla de relleno y pintura', 'N/A', USERS[1].id,20),
        Project("Limpieza", date.today(), date.today() + timedelta(days=1), CARS[2].license_plate, DEPARTMENTS[3].id,
        'Tapiceria embarrada de grasa', 'Limpieza completa', 'Asientos rotos', USERS[2].id, 32),
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
        Car('PTK630', 'Toyota', 'Hatchback', 2003,'LM97845U123136K', 'LM63845U123648S', 'azul', 'Raya en el capo', clients[0].id),
        Car('RT5031', 'Jeep', 'SUV', 2006,'GF97845U978456K', 'AR63845U123879D', 'amarillo', 'Limpieza de tapiceria', clients[1].id),
        Car('CX30EW', 'Nissan', 'Crossover', 2015,'HL9RT64897845ZF', 'PK61485G54387SA', 'amarillo', 'Croche', clients[2].id)
    ]
    db.session.add_all(cars)
    db.session.commit()

def create_default_departments():
    DEPARTMENTS = [
        Department('Latoneria'), Department('Pintura'), Department('Mecanica'),
        Department('Lavado') 
    ]
    db.session.add_all(DEPARTMENTS)
    db.session.commit()

def create_default_measures():
    MEASURES = [
        Measures(8, 'Pulgadas'), Measures(10, 'Pulgadas'), Measures(12, 'Pulgadas')
    ]
    db.session.add_all(MEASURES)
    db.session.commit()

def create_default_action_plans():
    USERS = db.session.query(User).all()
    ACTION_PLANS = [
        ActionPlan('Preparar la superficie', 'Lijado de superficie', date.today(), date.today() + timedelta(days=1), 20, USERS[0].id, 50, 2),
        ActionPlan('Preparar la superficie', 'Remover la pintura', date.today(), date.today() + timedelta(days=2), 20, USERS[1].id, 100, 2),
        ActionPlan('Preparar la superficie', 'Enmasillar', date.today(), date.today() + timedelta(days=5), 20, USERS[2].id, 120, 1)
    ]
    db.session.add_all(ACTION_PLANS)
    db.session.commit()

def create_default_human_talent():
    USERS = db.session.query(User).all()
    HUMAN_TALENT = [
        HumanTalent('Preparar la superficie', 'Lijado de superficie', 24, 2, 5, USERS[0].id, 50, 2),
        HumanTalent('Preparar la superficie', 'Remover la pintura', 24, 2, 5, USERS[1].id, 100, 2) ,
        HumanTalent('Preparar la superficie', 'Enmasillar', 24, 2, 5, USERS[2].id, 120, 1)
    ]
    db.session.add_all(HUMAN_TALENT)
    db.session.commit()

def create_default_materials():
    USERS = db.session.query(User).all()
    MEASURES = db.session.query(Measures).all()
    MATERIALS = [
        MaterialsSupplies('Preparar la superficie', 'Lijado de superficie', 'Insumo', 'Disco de lija', 5, MEASURES[0].id, 5, USERS[0].id, 120),
        MaterialsSupplies('Preparar la superficie', 'Remover la pintura', 'Insumo', 'Disco de lija', 5, MEASURES[0].id, 5, USERS[1].id, 120),
        MaterialsSupplies('Preparar la superficie', 'Enmasillar', 'Insumo', 'Disco de lija', 5, MEASURES[0].id, 5, USERS[2].id, 120)
    ]
    db.session.add_all(MATERIALS)
    db.session.commit()


def init_db_records():
    create_default_users()    
    create_default_clients()
    create_default_departments()
    create_default_projects()
    create_default_measures()
    create_default_action_plans()
    create_default_human_talent()
    create_default_materials()
    '''
    project = db.session.query(Project).filter_by(id=1).first()
    users = db.session.query(User).all()
    project.users.extend(users[1:])

    project = db.session.query(Project).filter_by(id=2).first()
    project.users.extend(users[2:])    

    user = users[0]
    projects = db.session.query(Project).all()
    user.projects.extend(projects)'''
    db.session.commit()



def init_db():
    db.create_all()
    init_db_records()
