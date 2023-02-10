from flask import render_template, request, session, redirect, url_for, flash
from sqlalchemy import select
from src.models import db
from src.models.User import User
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

        logged_user = db.session.query(User).filter_by(username=username).first()
        print(logged_user)
        print(password)
        print(check_password_hash(logged_user.password, password))
        if logged_user is None:
            error = 'Username does not exist.'
        elif not check_password_hash(logged_user.password, password):
            error = 'Incorrect password.'

        if error is None:
            return redirect(url_for('users_lists'))

        flash(error)

    return redirect(url_for('login'))