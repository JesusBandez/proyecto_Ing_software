from flask import render_template, request, session, redirect, url_for, flash
from sqlalchemy import select
from src.models import db
from src.models import User
from werkzeug.security import check_password_hash
from . import app

@app.route('/login')
def login():
    return render_template('login/login.html')

@app.route('/login', methods=('GET', 'POST'))
def log_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        logged_user = User.User.query.filter_by(username=username).first()
        print(logged_user)
        print(logged_user.password)
        print(check_password_hash(logged_user.password, password))

        if logged_user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(logged_user.password, password):
            error = 'Incorrect password.'

        if error is None:
            redirect(url_for('users_lists'))

    return redirect(url_for('users_lists'))