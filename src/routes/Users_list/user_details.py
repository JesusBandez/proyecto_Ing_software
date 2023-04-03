from flask import render_template, request, session, redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.lib.class_create_button import ListProjectsOfUser


from src.routes.auth import has_role
from src.models import db
from src.models.Project import Project
from src.models.User import User
from datetime import datetime
import pdfkit
from . import app

def user_projects(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    projects = db.session.query(Project).all()
    A = ListProjectsOfUser(projects,user)
    projects_user_is = A.list_table()
    header = A.header
    return [projects_user_is,user,header]

@app.route('/users_list/user_details')
def user_details():
    """Renderiza la vista con la lista de proyectos de un usuario.
        El Id del usuario se obtiene por url args"""
    user_id = request.args['id']
    get = user_projects(user_id)
    projects_user_is = get[0]
    user = get[1]
    users_projects_list_header = get[2]
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
