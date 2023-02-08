from flask import render_template
from . import app

@app.route('/')
def login():
    return render_template(
        'login/login.html'       
    )