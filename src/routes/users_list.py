from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from src.models import User
from src.models import db
from . import app

@app.route('/users_list')
def users_lists():
    users = User.User.query.all()
    return render_template(
        'users_list/users_list.html',
        users=users
    )

@app.route('/users_list/delete', methods=['GET', 'POST'])
def delete_user():
    user_id = request.form['id']
    user = db.session.query(User.User).filter_by(id=user_id).first()
    print(user)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users_lists'))

@app.route('/users_list/new_user')
def new_user():
    return render_template('users_list/new_user.html')

@app.route('/users_list/add_new_user', methods=['POST'])
def add_new_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['permissions']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        user = db.session.query(User).filter_by(username=username).first()
        if user is not None:
            error = f'User {username} is already registered.'

        if error is None:
            user = User(username, generate_password_hash(password), role, False)
            db.session.add(user)
            db.session.commit()

    return redirect(url_for('users_lists'))