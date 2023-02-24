from flask import render_template, request, session, redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.routes.auth import has_role
from src.models import db
from src.models.Project import Project
from src.models.User import User
from datetime import datetime
import pdfkit
from . import app


@app.route('/projects/project_details')
def project_details():
    """Renderiza la vista con la lista de proyectos de un usuario.
        El Id del usuario se obtiene por url args"""
    
    users_projects_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'First name', 'class': 'col-6'},
        {'label': 'Last name', 'class': 'col-2'},
        {'label' : 'actions', 'class': 'col-1'} 
    ]

    project_id = request.args['id']
    project = db.session.query(Project).filter_by(id=project_id).first()
    
    users_list_body = []
    
    for user in project.users:    
        see_user = generate_action(user.id, 'user_details', 
            button_class='btn btn-info w-100',
            text_class="fa-solid fa-eye",
            title="View user details")

        users_list_body.append({
            'data' : [user.id, user.first_name, user.last_name],
            'actions' : [see_user]
        })

    return render_template('projects/project_details.html',
        context={
            'id' : project.id,
            'description' : project.description,
            'start_date' : project.start.strftime(f'%m-%d-%Y'),
            'finish_date' : project.finish.strftime(f'%m-%d-%Y')
        },   
        list_context= {
                'list_header': users_projects_list_header,
                'list_body' : users_list_body
            })
