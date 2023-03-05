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

# Clientes del sistema
@app.route('/clients/list', methods=('GET', 'POST'))
def clients_list():
    "Renderiza la lista con todos los clientes del sistema"

    clients_list_header = [
        {'label': 'Cedula', 'class': 'col-1'},
        {'label': 'Name', 'class': 'col-1'},
        {'label': 'Lastname', 'class': 'col-1'},
        {'label': 'Birthdate', 'class': 'col-1'},
        {'label': 'Phone Number', 'class': 'col-2'},
        {'label': 'Mail', 'class': 'col-2'},
        {'label': 'Address', 'class': 'col-2'},
        {'label': 'Actions', 'class': 'col-2'}, 
    ]

    CLIENTS = db.session.query(Client).all()
    clients_list_body = []
    for client in CLIENTS:
        add_car = generate_action(client.id, 'new_car', method='get',
            button_class='btn btn-sm btn-outline-primary',
            text_class='fa fa-car',
            title="Add Car Information")

        edit = generate_action(client.id, 'edit_client', method='post', 
            button_class='btn btn-sm btn-outline-success',
            title="Edit client",
            text_class='fa-solid fa-pencil')

        remove = generate_action(client.id, 'remove_client', 'post',
            button_class='btn btn-sm btn-outline-danger',
            title="Remove client",
            text_class='fa-solid fa-trash')
        
        clients_list_body.append({
            'data' : [client.ci, client.first_name, 
                    client.last_name, client.birth_date.strftime(f'%m-%d-%Y'), client.phone, client.mail, client.address],
            'actions' : [add_car, edit, remove]
            })
     
    return render_template('clients/clients.html',
        has_role=has_role,
        list_context= {
                'list_header': clients_list_header,
                'list_body' : clients_list_body
            })

# Agregar proyectos
@app.route('/clients/new_clients')
def new_client():    
    "Muestra el formulario para agregar o editar un proyecto"
    return render_template('clients/new_client.html')

@app.route('/clients/new_client/add_client', methods=['POST'])
def add_new_client():
    """Obtiene los datos para agregar un nuevo carro de un cliente y 
        lo agrega al sistema"""
    ci = request.form['ci']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    birth_date = datetime.strptime(request.form['birth_date'], r'%Y-%m-%d')
    phone = request.form['phone']
    mail = request.form['mail']
    address = request.form['address']
    
    client = Client(ci, first_name, last_name, birth_date, mail, phone, address)        
    time_data = datetime.now()
    date = time_data.strptime(time_data.strftime(r'%Y-%m-%d'), r'%Y-%m-%d')
    hour = time_data.strptime(time_data.strftime(r'%H:%M:%S'), r'%H:%M:%S')
    log = Logger('Adding Client', date, hour)
    db.session.add(log)
    db.session.add(client)
        
    db.session.commit()        
    return redirect(url_for('clients_list'))

@app.route('/clients/list/remove_project', methods=['GET', 'POST'])
def remove_client():
    "Eliminar client"
    client_id = request.form['id']
    client = db.session.query(Client).filter_by(id=client_id).first()
    time_data = datetime.now()
    date = time_data.strptime(time_data.strftime(r'%Y-%m-%d'), r'%Y-%m-%d')
    hour = time_data.strptime(time_data.strftime(r'%H:%M:%S'), r'%H:%M:%S')
    log = Logger('Deleting project', date, hour)

    db.session.add(log)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('clients_list'))

@app.route('/clients/new_car', methods=['GET', 'POST'])
def new_car():    
    """Muestra el formulario para agregar carro de un cliente y los carros
        que tiene el mismo"""
    cars_projects_list_header = [
        {'label': 'Placa', 'class': 'col-1'},
        {'label': 'Marca', 'class': 'col-6'},
        {'label': 'Modelo', 'class': 'col-2'},
        {'label': 'Año', 'class': 'col-2'},
        {'label': 'Serial de Carroceria', 'class': 'col-2'},
        {'label': 'Serial de Motor', 'class': 'col-2'},
        {'label': 'Color', 'class': 'col-2'},
        {'label': 'Problema', 'class': 'col-2'}
    ]

    client_id = request.args['id']
    client = db.session.query(Client).filter_by(id=client_id).first() 
    clients_cars = []
    for car in client.cars :
        clients_cars.append({
            'data' : [car.license_plate, car.brand, car.model, car.year,
                        car.serial_car, car.serial_engine, car.color, car.issue]
        })
        
    return render_template('clients/new_car.html', 
                list_context= {
                'list_header': cars_projects_list_header,
                'list_body' : clients_cars
            })

@app.route('/clients/new_car/add_car', methods=['GET', 'POST'])
def add_new_car():
    """ Obtiene los datos para agregar un nuevo carro de un cliente y 
        lo agrega al sistema """
    ci_owner = request.form['ci_owner']
    license_plate = request.form['license_plate']
    brand = request.form['brand']
    model = request.form['model']
    year = request.form['year']
    serial_car = request.form['serial_car']
    serial_engine = request.form['serial_engine']
    color = request.form['color']
    issue = request.form['issue']
    owner = db.session.query(Client).filter_by(ci=ci_owner).first()
    print(owner)

    car = Car(license_plate, brand, model, year, serial_car, serial_engine, color, issue, owner.id)
    time_data = datetime.now()
    date = time_data.strptime(time_data.strftime(r'%Y-%m-%d'), r'%Y-%m-%d')
    hour = time_data.strptime(time_data.strftime(r'%H:%M:%S'), r'%H:%M:%S')
    log = Logger('Adding new car', date, hour)
    db.session.add(log)
    db.session.add(car)
        
    db.session.commit()  
    return redirect(url_for('clients_list'))

@app.route('/clients/list/edit_client', methods=['POST'])
def edit_client():
    "Editar proyecto"
    """ if not has_role('admin'):
        return redirect(url_for()) 
    project = db.session.query(Project).filter_by(
        id=request.form['id']).first()
    edit_context = {
        'id' : project.id,
        'description': project.description,
        'start' : project.start.date(),
        'finish' : project.finish.date(),
        'users' : project.users
    } """
    print("editing project")
    return redirect(url_for('clients_list'))
