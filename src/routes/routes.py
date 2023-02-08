from flask import render_template
from main import app

@app.route('/')
def home():
    return render_template(
        'login.html'       
    )