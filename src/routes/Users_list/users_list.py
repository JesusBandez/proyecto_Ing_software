from flask import render_template, redirect, url_for, request, flash, session
from src.routes.auth import has_role
from src.routes.Users_list import user_details
from src.models.User import User
from src.models.Logger import Logger
from src.models import db
from src.lib.generate_action import generate_action
from . import app

def search_users(typeS,search):
    if typeS == "login":
        users = db.session.query(User).filter(User.username.ilike(search))
    elif typeS == "first":
        users = db.session.query(User).filter(User.first_name.ilike(search))
    elif typeS == "last":
        users = db.session.query(User).filter(User.last_name.ilike(search))
    elif typeS == "role":
        users = db.session.query(User).filter(User.job.ilike(search))
    else:
        users = db.session.query(User).all()
    return users


@app.route('/users_list', methods=['GET', 'POST'])
def users_lists():
    "Muestra la lista de usuarios del sistema"

    users_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'Login', 'class': 'col-2'},
        {'label': 'First name', 'class': 'col-2'},
        {'label': 'Last name', 'class': 'col-2'},
        {'label': 'Role', 'class': 'col-2'},
        {'label': 'Actions', 'class': 'col-2'}
    ]
    try:
        typeS = request.form['typeSearch']
        search = request.form['search']
        users = search_users(typeS,search)
        if users.count() == 0:
            users = db.session.query(User).all()
    except:
        users = db.session.query(User).all()

    users_list_body = []
    for user in users:
        # Mostrar boton de accion desabilitado si el usuario no tiene
        # permisos

        delete = generate_action(user.id, 'delete_user', 'post', 
            button_class='btn btn-outline-danger', text_class='fa fa-trash',
            title="Delete user",
            disabled=not has_role('admin'))           
        
        see_projects = generate_action(user.id, 'user_details', 'get',
                button_class='btn btn-outline-primary', text_class="fa-solid fa-eye",
                title="View the projects associated with the user") 

        users_list_body.append({
                'data' : [user.id, user.username, user.first_name, 
                          user.last_name, user.job],               
                'actions' : [delete, see_projects]})

    return render_template(
        'users_list/users_list.html',
        has_role=has_role,
        list_context= {
            'list_header': users_list_header,
            'list_body' : users_list_body,
        }       
    )

@app.route('/users_list/delete', methods=['GET', 'POST'])
def delete_user():
    "Elimina a un usuario del sistema"

    if not has_role('admin'):
        return redirect(url_for('error'))
        
    user_id = request.form['id']
    user = db.session.query(User).filter_by(id=user_id).first()

    log = Logger('Deleting user')

    db.session.add(log)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users_lists'))

@app.route('/users_list/new_user')
def new_user():
    "Renderiza el formulario de registro de nuevo usuario"

    if not has_role('admin'):
        return redirect(url_for('error'))

    return render_template('users_list/new_user.html')

@app.route('/users_list/add_new_user', methods=['POST'])
def add_new_user():
    "Agrega un nuevo usuario al sistema"

    f_name = request.form['f_name']
    l_name = request.form['l_name']
    job = request.form['job']
    username = request.form['username']
    password = request.form['password']
    role = request.form['permissions']

    error = None
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    user = db.session.query(User).filter_by(username=username).first()
    if user:
        error = f'Username "{username}" is already taken.'

    if error:
        flash(error)
        return redirect(url_for('new_user'))

    if error is None:
        user = User(f_name, l_name,username, password, role, job, False)

        log = Logger('Adding user')

        db.session.add(log)
        db.session.add(user)
        db.session.commit()       
        
    return redirect(url_for('users_lists'))