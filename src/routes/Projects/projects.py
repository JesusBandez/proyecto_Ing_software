from flask import render_template, request, session, redirect, url_for, flash
from src.models import db

from . import app


@app.route('/projects', methods=('GET', 'POST'))
def projects():   
    return render_template('projects/projects.html')