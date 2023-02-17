from flask import render_template, request, session, redirect, url_for, flash
from src.models import db

from . import app


@app.route('/projects', methods=('GET', 'POST'))
def projects():  
    users_list_header = [
        {'label': 'Id', 'style': 'width: 5%'},
        {'label': 'Description', 'style': 'width: 35%'},
        {'label': 'Start', 'style': 'width: 15%'},
        {'label': 'End', 'style': 'width: 15%'},
        {'label': 'Actions', 'style': 'width: 25%'},        
    ]
    return render_template('projects/projects.html',
        list_context= {
                'list_header': users_list_header,
                'list_body' : [], # Meterle los datos
            })