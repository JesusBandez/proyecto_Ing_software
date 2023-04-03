from flask import after_this_request, render_template, request, send_file, session, redirect, url_for, flash, send_from_directory
from src.lib.generate_action import generate_action
from src.lib.class_create_button import ListClientsCars

from src.routes.auth import has_role, decorator
from src.models import db
from src.models.Client import Client
from src.models.Car import Car
from src.models.Logger import Logger
from src.models.Project import Project
from src.models.Car import Car

from src.models.User import User
from sqlalchemy.exc import IntegrityError

from src.errors import Errors, ERROR_MUST_BE_ADMIN,ERROR_EXISTS_LICENSE_PLATE

from datetime import datetime
from . import app


def search_cars(typeS,search,client_id):
    client = db.session.query(Client).filter_by(id=client_id).first()
    if typeS == "number":
        cars_found = db.session.query(Car).filter_by(Car.license_plate.ilike(int(search)),Car.owner.like(client.id))
    elif typeS == "brand":
        cars_found = db.session.query(Car).filter(Car.brand.ilike(search),Car.owner.like(client.id))
    elif typeS == "model":
        cars_found = db.session.query(Car).filter(Car.model.ilike(search),Car.owner.like(client.id))
    elif typeS == "year":
        cars_found = db.session.query(Car).filter(Car.year.ilike(int(search)),Car.owner.like(client.id))
    elif typeS == "color":
        cars_found = db.session.query(Car).filter(Car.color.ilike(search),Car.owner.like(client.id))
    else:
        cars_found = client.cars
    return cars_found

@app.route('/clients/client_details', methods=('GET', 'POST'))
def client_details():
    client_id = request.args['id']

    try:
        typeS = request.form['typeSearch']
        search = request.form['search']
        cars_found = search_cars(typeS,search,client_id)
        if cars_found.count() == 0:
            client = db.session.query(Client).filter_by(id=client_id).first()
            cars_found = client.cars
    except:
        client = db.session.query(Client).filter_by(id=client_id).first()
        cars_found = client.cars

    
    client = db.session.query(Client).filter_by(id=client_id).first() 

    A = ListClientsCars(cars_found,client_id)
    clients_cars = A.list_table()
    cars_projects_list_header = A.header
        
    return render_template('clients/client_details.html',
                has_role=has_role,
                context={
                    'client' : client,
                },
                list_context= {
                'list_header': cars_projects_list_header,
                'list_body' : clients_cars
            })



@app.route('/clients/client_details/new_car', methods=['GET', 'POST'])
@decorator
def new_car():    
    """Muestra el formulario para agregar o editar el carro de un cliente"""
    car = db.session.query(Car).filter_by(
        license_plate=request.args.get('car_plate')).first()
    
    if car:
        page_title = 'Edit car'
    
    else:
        page_title = 'Add car'

    return render_template('clients/new_car.html',
            context={
                'id' : request.args['id'],
                'car' : car,
                'page_title' : page_title,
            })

def adding_new_car(car_to_edit,owner_id,owner,license_plate,brand,model,year,serial_engine,serial_car,color,issue):
    if car_to_edit:
        changes = {
            'license_plate' : license_plate,
            'brand' : brand,
            'model' : model,
            'year' : year,
            'serial_car' : serial_car,
            'serial_engine' : serial_engine,
            'color' : color,
            'issue' : issue,
        }
        
        car = db.session.query(Car).filter_by(
            license_plate=car_to_edit).update(changes)
        log = Logger('Editing new car')        
        db.session.add(log)

    else:
        car = Car(license_plate, brand, model, year, serial_car, serial_engine, color, issue, owner.id)
        log = Logger('Adding new car')
        db.session.add_all([log, car])

    #TODO: Mostrar un mensaje de error
    try:
        db.session.commit()
    except IntegrityError:
        return False

    return car


@app.route('/clients/client_details/add_car', methods=['GET', 'POST'])
@decorator
def add_new_car():
    """ Obtiene los datos para agregar un nuevo carro de un cliente y 
        lo agrega al sistema """ 
    car_to_edit = request.form.get('car_plate')
    owner_id = request.form['owner_id']
    owner = db.session.query(Client).filter_by(id=owner_id).first()

    license_plate = request.form['license_plate']
    brand = request.form['brand']
    model = request.form['model']
    year = request.form['year']
    serial_car = request.form['serial_car']
    serial_engine = request.form['serial_engine']
    color = request.form['color']
    issue = request.form['issue']

    c = adding_new_car(car_to_edit,owner_id,owner,license_plate,brand,model,year,serial_engine,serial_car,color,issue)

    return redirect(url_for('client_details', id=owner_id))

@decorator
def removing_car(license_plate,owner_id):
    car = db.session.query(Car).filter(
        Car.license_plate == license_plate,
        Car.owner == owner_id
        ).first()
    log = Logger('Deleting Car')

    db.session.add(log)
    db.session.delete(car)
    db.session.commit()
    return car


@app.route('/clients/client_details/remove_car', methods=['GET', 'POST'])
@decorator
def remove_car():
    "Eliminar carro"
    license_plate = request.form['id']
    owner_id = request.form['owner_id']

    c = removing_car(license_plate,owner_id)

    return redirect(url_for('client_details', id=request.form['owner_id']))