from flask import after_this_request, render_template, request,redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.routes.auth import has_role
from src.models.Client import Client
from src.routes.Clients import client_details
from src.models.Logger import Logger
from src.models import db

from datetime import datetime

from src.errors import Errors, ERROR_MUST_BE_ADMIN,ERROR_MUST_BE_ADMIN_ADD_CLIENT,ERROR_MUST_BE_ADMIN_DELETE_CLIENT, ERROR_CI_ALREADY_EXISTS

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
            title="See client information")

        edit = generate_action(client.id, 'new_client', method='get', 
            button_class='btn btn-sm btn-outline-success',
            title="Edit client",
            text_class='fa-solid fa-pencil',
            disabled= not has_role('opera'))

        remove = generate_action(client.id, 'remove_client', 'post',
            button_class='btn btn-sm btn-outline-danger',
            title="Remove client",
            text_class='fa-solid fa-trash',
            disabled= not has_role('opera'))
        
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
    if not has_role('opera'):
        title = Errors(ERROR_MUST_BE_ADMIN_ADD_CLIENT).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN_ADD_CLIENT).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('clients_list'))

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

def adding_client(client_to_edit,ci,first_name,last_name,birth_date,phone,mail,address):
    if not has_role('opera'):
        return False

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
        title = Errors(ERROR_CI_ALREADY_EXISTS).error.title
        desc = Errors(ERROR_CI_ALREADY_EXISTS).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('clients_list'))
    elif e[0] == False and e[1] == 1:
        title = Errors(ERROR_MUST_BE_ADMIN).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('clients_list'))
    

    if client_to_edit != None:
        return redirect(url_for('clients_list'))

    return redirect(url_for('client_details', id=e[1].id))


def removing_client(client_id):
    if not has_role('opera'):
        return False
    
    client = db.session.query(Client).filter_by(id=client_id).first()
    for car in client.cars:
        db.session.delete(car)
        
    log = Logger('Deleting client')
    db.session.add(log)
    db.session.delete(client)
    db.session.commit()
    return client

@app.route('/clients/list/remove_project', methods=['GET', 'POST'])
def remove_client():
    "Eliminar client"
    client_id = request.form['id']
    c = removing_client(client_id)
    if c == False:
        title = Errors(ERROR_MUST_BE_ADMIN_DELETE_CLIENT).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN_DELETE_CLIENT).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('clients_list'))

    return redirect(url_for('clients_list'))