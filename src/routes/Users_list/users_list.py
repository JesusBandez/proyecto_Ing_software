from flask import render_template, redirect, url_for, request, flash, session
from src.routes.auth import has_role
from src.routes.Users_list import user_details
from src.models.User import User
from src.models.Logger import Logger
from src.models import db
from src.lib.generate_action import generate_action

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

        delete = generate_action(user.id, 'delete_user', 'post', 
            button_class='btn btn-outline-danger', text_class='fa fa-trash',
            title="Delete user",
            disabled=not has_role('admin'))           
        
        see_user = generate_action(user.id, 'user_details', 'get',
                button_class='btn btn-outline-primary', text_class="fa-solid fa-eye",
                title="View the projects associated with the user")

        edit_user = generate_action(user.id, 'new_user', 'post',
                button_class='btn btn-outline-primary', text_class="fa-solid fa-pencil",
                title="Edit the user")

        users_list_body.append({
                'data' : [user.id, user.username, user.first_name, 
                          user.last_name, user.job],               
                'actions' : [see_user, edit_user, delete]})

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
def delete_user():
    "Elimina a un usuario del sistema"

    if not has_role('admin'):
        title = Errors(ERROR_MUST_BE_ADMIN_DELETE_USER).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN_DELETE_USER).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('users_lists'))
        
    user_id = request.form['id']
    z = deleting(user_id)
    
    return redirect(url_for('users_lists'))

@app.route('/users_list/new_user', methods=['POST', 'GET'])
def new_user():
    "Renderiza el formulario de registro de nuevo usuario"
    
    if not has_role('admin'):
        title = Errors(ERROR_MUST_BE_ADMIN_NEW_USER).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN_NEW_USER).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('users_lists'))

    
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

    if not client_to_edit:
        user = create_user(f_name, l_name,username, password, role, job)
        if user[1] == False:
            title = Errors(ERROR_USERNAME_ALREADY_USED).error.title
            desc = Errors(ERROR_USERNAME_ALREADY_USED).error.description
            flash(True, 'error')
            flash(title, 'error_title') 
            flash(desc, 'error_description')
            return redirect(url_for('new_user'))
    else:

        changes = {
            'first_name' : f_name,
            'last_name' : l_name,
            'job' : job,
            'username' : username,
            'password' : password,
            'role' : role,

        }
        db.session.query(User).filter_by(
            id=client_to_edit).update(changes)
        log = Logger('Editing user')
        db.session.add(log)

    db.session.commit()
    print('commit')
    return redirect(url_for('users_lists'))