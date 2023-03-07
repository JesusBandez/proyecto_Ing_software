from flask import after_this_request, render_template, request, send_file, session, redirect, url_for, flash, send_from_directory
from src.lib.generate_action import generate_action
from src.routes.auth import has_role
from src.models import db
from src.models.Client import Client
from src.models.Car import Car
from src.models.Logger import Logger
from src.models.Project import Project
from src.models.User import User

from src.routes.Clients import client_details

from datetime import datetime
from . import app


def search_clients(typeS,search):
    if typeS == "ci":
        users = db.session.query(Client).filter(Client.ci.ilike(search))
    elif typeS == "name":
        users = db.session.query(Client).filter(Client.first_name.ilike(search))
    elif typeS == "last":
        users = db.session.query(Client).filter(Client.last_name.ilike(search))
    elif typeS == "mail":
        users = db.session.query(Client).filter(Client.mail.ilike(search))
    elif typeS == "phone":
        users = db.session.query(Client).filter(Client.phone.ilike(search))
    else:
        users = db.session.query(Client).all()
    return users


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

    try:
        typeS = request.form['typeSearch']
        search = request.form['search']
        CLIENTS = search_clients(typeS,search)
        if CLIENTS.count() == 0:
            CLIENTS = db.session.query(Client).all()
    except:
        CLIENTS = db.session.query(Client).all()

    clients_list_body = []
    for client in CLIENTS:
        see_cars = generate_action(client.id, 'client_details', method='get',
            button_class='btn btn-sm btn-outline-primary',
            text_class='fa fa-car',
            title="Add Car Information")

        edit = generate_action(client.id, 'new_client', method='get', 
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
            'actions' : [see_cars, edit, remove]
            })
     
    return render_template('clients/clients.html',
        has_role=has_role,
        list_context= {
                'list_header': clients_list_header,
                'list_body' : clients_list_body
            })

# Agregar clientes
@app.route('/clients/new_clients')
def new_client():    
    "Muestra el formulario para agregar o editar un cliente"
    client = None
    birthdate = None
    if request.args.get('id'):
        client = db.session.query(Client).filter_by(id=request.args.get('id')).first()
        page_title = 'Edit client'
        birthdate = client.birth_date.date()

    else:
        page_title = 'Add new client'
    
    return render_template('clients/new_client.html', context={
        'client' : client,
        'birthdate' : birthdate,
        'page_title' : page_title, 
    })

@app.route('/clients/new_client/add_client', methods=['POST'])
def add_new_client():
    """Obtiene los datos para agregar un nuevo carro de un cliente y 
        lo agrega al sistema"""
    
    client_to_edit = request.form.get('client_to_edit')
    ci = request.form['ci']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    birth_date = datetime.strptime(request.form['birth_date'], r'%Y-%m-%d')
    phone = request.form['phone']
    mail = request.form['mail']
    address = request.form['address']
    
    if not client_to_edit:
        client = Client(ci, first_name, last_name, birth_date, mail, phone, address)
        time_data = datetime.now()
        date = time_data.strptime(time_data.strftime(r'%Y-%m-%d'), r'%Y-%m-%d')
        hour = time_data.strptime(time_data.strftime(r'%H:%M:%S'), r'%H:%M:%S')
        log = Logger('Adding Client', date, hour)
        db.session.add(log)
        db.session.add(client)
        db.session.flush()
        db.session.refresh(client)
        id = client.id
    
    else:
        changes = {
            'ci' : ci,
            'first_name' : first_name,
            'last_name' : last_name,
            'birth_date' : birth_date,
            'mail' : phone,
            'phone' : mail,
            'address' : address,
        }
        client = db.session.query(Client).filter_by(
            id=client_to_edit).update(changes)

        id = client_to_edit
        time_data = datetime.now()
        date = time_data.strptime(time_data.strftime(r'%Y-%m-%d'), r'%Y-%m-%d')
        hour = time_data.strptime(time_data.strftime(r'%H:%M:%S'), r'%H:%M:%S')
        log = Logger('Editing project', date, hour)
        db.session.add(log)
        
    db.session.commit()        
    return redirect(url_for('client_details', id=id))

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

