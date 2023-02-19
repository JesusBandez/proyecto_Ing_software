from flask import render_template, request, session, redirect, url_for, flash
from src.models import db
from src.models.User import User
from werkzeug.security import check_password_hash
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

        logged_user = query.first()

        if logged_user is None:
            error = 'Username does not exist.'
        elif not check_password_hash(logged_user.password, password):
            error = 'Incorrect password.'

        if error is None:
            query.update(
                {'status' : True}
            )
            db.session.commit()
            session['user'] = {
                'username' : username,
                'role' : logged_user.role
            }
            return redirect(url_for('user_projects', id=logged_user.id))

        flash(error)
    return render_template('login/login.html')


@app.route('/logout')
def logout():
    db.session.query(User).filter_by(
        username=session['user']['username']
        ).update( {'status' : False})
    db.session.commit()
    session.pop('user')
    
    return redirect(url_for('login'))