from flask import render_template, request, session, redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.routes.auth import has_role
from src.models import db
from src.models.Project import Project
from src.models.User import User
from datetime import datetime
import pdfkit
from . import app


@app.route('/users_list/user_details')
def user_details():
    """Renderiza la vista con la lista de proyectos de un usuario.
        El Id del usuario se obtiene por url args"""
    
    users_projects_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'Description', 'class': 'col-6'},
        {'label': 'Start', 'class': 'col-2'},
        {'label': 'End', 'class': 'col-2'},
        {'label' : 'actions', 'class': 'col-1'} 
    ]

    user_id = request.args['id']
    user = db.session.query(User).filter_by(id=user_id).first()
    projects = db.session.query(Project).all()    
    projects_user_is = []
    for p in projects :
        for u in p.users:
            
            see_project = generate_action(p.id, 'project_details', 
                button_class='btn btn-info w-100',
                text_class="fa-solid fa-eye",
                title="View project details")
            if (u.id == user.id):
                projects_user_is.append({
                    'data' : [p.id, p.description, p.start.strftime(f'%m-%d-%Y'), p.finish.strftime(f'%m-%d-%Y')],
                    'actions' : [see_project]
                })

    return render_template('users_list/user_details.html',
        context={
            'username' : user.username,
            'fname' : user.first_name,
            'lname' : user.last_name,
            'job' : user.job
        },   
        list_context= {
                'list_header': users_projects_list_header,
                'list_body' : projects_user_is
            })
