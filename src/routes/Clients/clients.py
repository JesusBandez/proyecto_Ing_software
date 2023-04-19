from flask import after_this_request, render_template, request,redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.lib.class_create_button import ListClients

from src.routes.auth import has_role, require_permissions,error_display
from src.models.Client import Client
from src.routes.Clients import client_details
from src.models.Logger import Logger
from src.models import db

from datetime import datetime

from src.errors import Errors, ERROR_MUST_BE_ADMIN,ERROR_MUST_BE_ADMIN_ADD_CLIENT,ERROR_MUST_BE_ADMIN_DELETE_CLIENT, ERROR_CI_ALREADY_EXISTS

from . import app


def search_clients(typeS,search):
    if typeS == "ci":
        users = db.session.query(Client).filter(Client.ci.ilike(f'%{search}%'))
    elif typeS == "name":
        users = db.session.query(Client).filter(Client.first_name.ilike(f'%{search}%'))
    elif typeS == "last":
        users = db.session.query(Client).filter(Client.last_name.ilike(f'%{search}%'))
    elif typeS == "mail":
        users = db.session.query(Client).filter(Client.mail.ilike(f'%{search}%'))
    elif typeS == "phone":
        users = db.session.query(Client).filter(Client.phone.ilike(f'%{search}%'))
    else:
        users = db.session.query(Client).all()
    return users


# Clientes del sistema
@app.route('/clients/list', methods=('GET', 'POST'))
def clients_list():
    "Renderiza la lista con todos los clientes del sistema"

    try:
        typeS = request.form['typeSearch']
        search = request.form['search']
        CLIENTS = search_clients(typeS,search)
        if CLIENTS.count() == 0:
            CLIENTS = db.session.query(Client).all()
    except:
        CLIENTS = db.session.query(Client).all()

    A = ListClients(CLIENTS)
    clients_list_body = A.list_table()
    clients_list_header = A.header
    return render_template('clients/clients.html',
        has_role=has_role,
        list_context= {
                'list_header': clients_list_header,
                'list_body' : clients_list_body
            })

# Agregar clientes
@app.route('/clients/new_clients')
@require_permissions
def new_client():
    "Muestra el formulario para agregar o editar un cliente"

    client = db.session.query(Client).filter_by(id=request.args.get('id')).first()
    birthdate = None
    if client:        
        page_title = 'Edit client'
        birthdate = client.birth_date.date()

    else:
        page_title = 'Add new client'
    
    return render_template('clients/new_client.html', context={
        'client' : client,
        'birthdate' : birthdate,
        'page_title' : page_title, 
    })

@require_permissions
def adding_client(client_to_edit,ci,first_name,last_name,birth_date,phone,mail,address):
    if not client_to_edit:
        client = Client(ci, first_name, last_name, birth_date, mail, phone, address)
        log = Logger('Adding Client')
        db.session.add_all([log, client])        
        db.session.flush()
        db.session.refresh(client)
    
    else:
        changes = {
            'ci' : ci,
            'first_name' : first_name,
            'last_name' : last_name,
            'birth_date' : birth_date,
            'mail' : mail,
            'phone' : phone,
            'address' : address,
        }
        client = db.session.query(Client).filter_by(
            id=client_to_edit).update(changes)
        client = db.session.query(Client).filter_by(
            id=client_to_edit).first()

        log = Logger('Editing project')
        db.session.add(log)
        
    db.session.commit()
    return client

def verify_client_exist(CI,client_to_edit):
    if client_to_edit is not None:
        client_id = int(client_to_edit)
    else:
        return False
    client = db.session.query(Client).filter_by(ci=CI).first()
    if client!=None and client_id != client.id:
        return True
    return False

def editing_client(ci,client_to_edit,first_name,last_name,birth_date,phone,mail,address):
    already_exists = verify_client_exist(ci,client_to_edit)

    if already_exists:
        return [False,0]

    c = adding_client(client_to_edit,ci,first_name,last_name,birth_date,phone,mail,address)

    if c==False:
        return [False,1]

    return [True,c]


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

    e = editing_client(ci,client_to_edit,first_name,last_name,birth_date,phone,mail,address)

    if e[0] == False and e[1] == 0:
        error_display(ERROR_CI_ALREADY_EXISTS)
        return redirect(url_for('clients_list'))
    elif e[0] == False and e[1] == 1:
        error_display(ERROR_MUST_BE_ADMIN)
        return redirect(url_for('clients_list'))

    if client_to_edit != None:
        return redirect(url_for('clients_list'))

    return redirect(url_for('client_details', id=e[1].id))

@require_permissions
def removing_client(client_id):    
    client = db.session.query(Client).filter_by(id=client_id).first()
    for car in client.cars:
        db.session.delete(car)
        
    log = Logger('Deleting client')
    db.session.add(log)
    db.session.delete(client)
    db.session.commit()
    return client

@app.route('/clients/list/remove_project', methods=['GET', 'POST'])
@require_permissions
def remove_client():
    "Eliminar client"
    client_id = request.form['id']
    c = removing_client(client_id)

    return redirect(url_for('clients_list'))