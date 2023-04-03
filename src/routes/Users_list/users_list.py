from flask import render_template, redirect, url_for, request, flash, session
from src.routes.auth import has_role, require_permissions, error_display
from src.routes.Users_list import user_details

from src.lib.class_create_button import ListUsersList

from src.models.User import User
from src.models.Logger import Logger
from src.models import db
from src.lib.generate_action import generate_action
from werkzeug.security import generate_password_hash
from src.errors import Errors, ERROR_MUST_BE_ADMIN, ERROR_MUST_BE_ADMIN_NEW_USER,ERROR_MUST_BE_ADMIN_DELETE_USER, ERROR_USERNAME_ALREADY_USED

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
    #"Muestra la lista de usuarios del sistema"
    try:
        typeS = request.form['typeSearch']
        search = request.form['search']
        users = search_users(typeS,search)
        if users.count() == 0:
            users = db.session.query(User).all()
    except:
        users = db.session.query(User).all()

    A = ListUsersList(users)
    users_list_body = A.list_table()
    users_list_header = A.header

    return render_template(
        'users_list/users_list.html',
        has_role=has_role,
        list_context= {
            'list_header': users_list_header,
            'list_body' : users_list_body,
        })

def deleting(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()

    log = Logger('Deleting user')

    db.session.add(log)
    db.session.delete(user)
    db.session.commit()
    return [log,user]

@app.route('/users_list/delete', methods=['GET', 'POST'])
@require_permissions
def delete_user():
    "Elimina a un usuario del sistema"
        
    user_id = request.form['id']
    z = deleting(user_id)
    
    return redirect(url_for('users_lists'))


@app.route('/users_list/new_user', methods=['POST', 'GET'])
@require_permissions
def new_user():
    "Renderiza el formulario de registro de nuevo usuario"
    
    user_to_edit = db.session.query(User).filter_by(
            id=request.form.get('id')).first()

    if not user_to_edit:
        title = 'Register New User'
    else:
        title = 'Edit User'


    return render_template('users_list/new_user.html', 
        context={
            'user_to_edit': user_to_edit,
            'title': title,
        })


def create_user(f_name, l_name,username, password, role, job):
    error = None
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    user = db.session.query(User).filter_by(username=username).first()
    if user:
        error = f'Username "{username}" is already taken.'

    if error:
        return [error,False]

    if error is None:
        user = User(f_name, l_name,username, password, role, job, False)

        log = Logger('Adding user')

        db.session.add(log)
        db.session.add(user)
        db.session.commit()
        return [user,True]


def verify_user_exist(guser_id,username):
    if guser_id is not None:
        user_id = int(guser_id)
    else:
        return False
    user = db.session.query(User).filter_by(id=user_id).first()
    if user!=None and username != user.username:
        return True
    return False


@app.route('/users_list/add_new_user', methods=['POST'])
def add_new_user():
    "Agrega un nuevo usuario al sistema"

    f_name = request.form['f_name']
    l_name = request.form['l_name']
    job = request.form['job']
    username = request.form['username']
    password = request.form['password']
    role = request.form['permissions']
    
    client_to_edit = request.form.get('user_to_edit')

    already_exists = verify_user_exist(client_to_edit,username)

    if already_exists:
        error_display(ERROR_USERNAME_ALREADY_USED)
        return redirect(url_for('users_lists'))

    if not client_to_edit:
        user = create_user(f_name, l_name,username, password, role, job)
        if user[1] == False:
            error_display(ERROR_USERNAME_ALREADY_USED)
            return redirect(url_for('new_user'))
    else:

        changes = {
            'first_name' : f_name,
            'last_name' : l_name,
            'job' : job,
            'username' : username,
            'password' : generate_password_hash(password),
            'role' : role,

        }
        db.session.query(User).filter_by(
            id=client_to_edit).update(changes)
        log = Logger('Editing user')
        db.session.add(log)

    db.session.commit()

    return redirect(url_for('users_lists'))