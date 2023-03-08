from flask import render_template, request, session, redirect, url_for, flash
from src.models import db
from src.models.User import User
from src.models.Logger import Logger
from werkzeug.security import check_password_hash
from datetime import date, datetime

from src.errors import Errors, ERROR_USERNAME_DONT_EXIST, ERROR_INCORRECT_PASSWORD,ERROR_MUST_BE_ADMIN

from . import app


@app.route('/login', methods=('GET', 'POST'))
def login():
    # If there is a user already loged in, redirect to users lists
    if session.get('user'):
        return redirect(url_for('users_lists'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        query = db.session.query(User).filter_by(username=username)
        title = ""
        desc = ""

        logged_user = query.first()

        if logged_user is None:
            error = True
            title = Errors(ERROR_USERNAME_DONT_EXIST).error.title
            desc = Errors(ERROR_USERNAME_DONT_EXIST).error.description
        elif not check_password_hash(logged_user.password, password):
            error = True
            title = Errors(ERROR_INCORRECT_PASSWORD).error.title
            desc = Errors(ERROR_INCORRECT_PASSWORD).error.description

        if error is None:
            query.update(
                {'status' : True}
            )
            log = Logger('Login')
            db.session.add(log)
            db.session.commit()
            session['user'] = {
                'id' : logged_user.id,
                'username' : username,
                'role' : logged_user.role
            }
            return redirect(url_for('user_details', id=logged_user.id))
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')

    return render_template('login/login.html')


@app.route('/logout')
def logout():
    db.session.query(User).filter_by(
        username=session['user']['username']
        ).update( {'status' : False})
    db.session.query(Logger).delete()
    db.session.commit()
    session.pop('user')
    
    return redirect(url_for('login'))