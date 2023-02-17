from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash
from src.routes.auth import has_role 
from src.models.User import User
from src.models import db
from src.lib.generate_action import generate_action
from . import app

@app.route('/users_list')
def users_lists():
    users_list_header = [
        {'label': 'Username', 'style': 'width: 65%'},
        {'label': 'Permissions', 'style': 'width: 25%'},
        {'label': 'Actions', 'style': 'width: 10%'}
    ]
    
    users = db.session.query(User).all()
    users_list_body = []
    for user in users:
        if not session.get('user') or session['user']['role'] == 'user':
            delete = generate_action(
                button_class='btn btn-danger', text_class='fa fa-trash', 
                disabled=True)
          
        else:
            delete = generate_action(user.id, 'delete_user',
                button_class='btn btn-danger', text_class='fa fa-trash')

        users_list_body.append({
                'data' : [user.username,user.role],               
                'actions' : [delete]})


    return render_template(
        'users_list/users_list.html',
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
        user = User(username, generate_password_hash(password), role, False)
        db.session.add(user)
        db.session.commit()       
        
    return redirect(url_for('users_lists'))