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
        {'label': 'Año', 'class': 'col-1'},
        {'label': 'Serial de Carroceria', 'class': 'col-1'},
        {'label': 'Serial de Motor', 'class': 'col-1'},
        {'label': 'Color', 'class': 'col-1'},
        {'label': 'Problema', 'class': 'col-5'}
    ]
    client_id = request.args['id']
    client = db.session.query(Client).filter_by(id=client_id).first() 
    clients_cars = []
    for car in client.cars :
        clients_cars.append({
            'data' : [car.license_plate, car.brand, car.model, car.year,
                        car.serial_car, car.serial_engine, car.color, car.issue]
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



@app.route('/clients/new_car', methods=['GET', 'POST'])
def new_car():    
    """Muestra el formulario para agregar carro de un cliente y los carros
        que tiene el mismo"""
        
    return render_template('clients/new_car.html',
            context={
                'id' : request.args['id']
            }
            )

@app.route('/clients/new_car/add_car', methods=['GET', 'POST'])
def add_new_car():
    """ Obtiene los datos para agregar un nuevo carro de un cliente y 
        lo agrega al sistema """
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

    car = Car(license_plate, brand, model, year, serial_car, serial_engine, color, issue, owner.id)
    time_data = datetime.now()
    date = time_data.strptime(time_data.strftime(r'%Y-%m-%d'), r'%Y-%m-%d')
    hour = time_data.strptime(time_data.strftime(r'%H:%M:%S'), r'%H:%M:%S')
    log = Logger('Adding new car', date, hour)
    db.session.add(log)
    db.session.add(car)
        
    db.session.commit()  
    return redirect(url_for('client_details', id=owner_id))