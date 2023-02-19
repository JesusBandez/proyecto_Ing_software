from flask import render_template, redirect, url_for, request, flash, session
from src.routes.auth import has_role
from src.models.User import User
from src.models import db
from src.lib.generate_action import generate_action
from . import app

@app.route('/users_list')
def users_lists():
    users_list_header = [
        {'label': 'Id', 'style': 'width: 5%'},
        {'label': 'Login', 'style': 'width: 20%'},
        {'label': 'First name', 'style': 'width: 17%'},
        {'label': 'Last name', 'style': 'width: 17%'},
        {'label': 'Role', 'style': 'width: 21%'},
        {'label': 'Actions', 'style': 'width: 10%'}
    ]

    users = db.session.query(User).all()
    users_list_body = []
    for user in users:
        # Mostrar boton de accion desabilitado si el usuario no tiene
        # permisos
        if has_role('admin'):
            delete = generate_action(user.id, 'delete_user', 'post',
                button_class='btn btn-danger', text_class='fa fa-trash')
            
                    
        else:
            delete = generate_action(
                button_class='btn btn-danger', text_class='fa fa-trash', 
                disabled=True)  

        users_list_body.append({
                'data' : [user.id, user.username, user.first_name, 
                          user.last_name, user.job],               
                'actions' : [delete]})

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
    if not has_role('admin'):
        return redirect(url_for('users_lists'))
        
    user_id = request.form['id']
    user = db.session.query(User).filter_by(id=user_id).first()

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users_lists'))

@app.route('/users_list/new_user')
def new_user():
    if not has_role('admin'):
        return redirect(url_for('users_lists'))

    return render_template('users_list/new_user.html')

@app.route('/users_list/add_new_user', methods=['POST'])
def add_new_user():    
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
        db.session.add(user)
        db.session.commit()       
        
    return redirect(url_for('users_lists'))