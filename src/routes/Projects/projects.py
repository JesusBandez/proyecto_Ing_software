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


@app.route('/projects/new_project', methods=('GET', 'POST'))
def new_project():     
    return render_template('projects/new_project.html')

@app.route('/projects/add_new_project', methods=['POST'])
def add_new_project():    
    dummy = request.form['Dummy']
    print(dummy)   
        
    return redirect(url_for('projects'))