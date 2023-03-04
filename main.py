from flask import Flask, redirect, render_template, url_for
from src.config import DevConfig
from src.models import db

app = Flask(__name__, template_folder='src/templates')
app.config.from_object(DevConfig)
from src.routes.Login import login
from src.routes.Users_list import users_list
from src.routes.Projects import projects
from src.routes.Logger import logger
from src.routes.Clients import clients


db.init_app(app)
if __name__== '__main__':
    app.run()

@app.route('/')
def root():        
    return redirect(url_for('login'))

@app.route('/error')
def error():
    return render_template('generics/generic_error.html')