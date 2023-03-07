from flask import after_this_request, render_template, request, send_file, session, redirect, url_for, flash, send_from_directory
from src.lib.generate_action import generate_action
from src.routes.auth import has_role
from src.models import db
from src.models.Client import Client
from src.models.Car import Car
from src.models.Logger import Logger
from src.models.Project import Project
from src.models.User import User

from datetime import datetime
from . import app

@app.route('/clients/client_details', methods=('GET', 'POST'))
def client_details():
    cars_projects_list_header = [
        {'label': 'Placa', 'class': 'col-1'},
        {'label': 'Marca', 'class': 'col-2'},
        {'label': 'Modelo', 'class': 'col-1'},
        {'label': 'Color', 'class': 'col-1'},
        {'label': 'Problema', 'class': 'col-5'},
        {'label': 'actions', 'class': 'col-1'}
    ]
    client_id = request.args['id']
    client = db.session.query(Client).filter_by(id=client_id).first() 
    clients_cars = []
    for car in client.cars :
        remove_car = generate_action(car.license_plate, 'remove_car', 
            method='post', 
            button_class='btn btn-sm btn-outline-danger',
            text_class='fa-solid fa-trash',
            title='View user details',
            disabled= not has_role('admin'),
            hiddens= [{'name' : 'owner_id', 'data': client_id}])

        edit = generate_action(car.license_plate, 'new_car', 
            method='get', 
            button_class='btn btn-sm btn-outline-success',
            title="Edit project",
            text_class='fa-solid fa-pencil',
            disabled= not has_role('admin'),
            hiddens= [{'name' : 'id', 'data': client_id}],
            value_name='car_plate')

        clients_cars.append({
            'data' : [car.license_plate, car.brand, car.model, 
                        car.color.capitalize(), car.issue],
            'actions' : [edit, remove_car]
        })
        
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
def new_car():    
    """Muestra el formulario para agregar o editar el carro de un cliente"""
    if not has_role('admin'):
            return redirect(url_for('error'))
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

@app.route('/clients/client_details/add_car', methods=['GET', 'POST'])
def add_new_car():
    """ Obtiene los datos para agregar un nuevo carro de un cliente y 
        lo agrega al sistema """
    if not has_role('admin'):
        return redirect(url_for('error'))        

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

    db.session.commit()  
    return redirect(url_for('client_details', id=owner_id))

@app.route('/clients/client_details/remove_car', methods=['GET', 'POST'])
def remove_car():
    "Eliminar carro"
    if not has_role('admin'):
        return redirect(url_for('error'))

    car = db.session.query(Car).filter(
        Car.license_plate == request.form['id'],
        Car.owner == request.form['owner_id']
        ).first()
    log = Logger('Deleting Car')

    db.session.add(log)
    db.session.delete(car)
    db.session.commit()
    return redirect(url_for('client_details', id=request.form['owner_id']))