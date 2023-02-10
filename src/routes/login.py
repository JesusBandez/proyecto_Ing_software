from flask import render_template, request, session
from sqlalchemy import select
from src.models import db
from src.models import User
from werkzeug.security import check_password_hash
from . import app

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = User.query.filter_by(username=username).all()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

    return render_template('login/login.html')