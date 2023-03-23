from flask import render_template, request, session, redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.routes.auth import has_role, is_project_manager
from src.models import db
from src.models.Project import Project
from src.models.User import User
from src.models.Logger import Logger
from datetime import datetime

from src.errors import Errors, ERROR_MUST_BE_ADMIN, ERROR_MUST_BE_ADMIN_AND_MANAGER


from . import app

@app.route('/projects/project_details')
def project_details():
    """Renderiza la vista con la lista de proyectos de un usuario.
        El Id del usuario se obtiene por url args"""
    
    users_projects_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'First name', 'class': 'col-3'},
        {'label': 'Last name', 'class': 'col-3'},
        {'label' : 'Job', 'class' : 'col-3'},
        {'label' : 'Actions', 'class': 'col-1'} 
    ]


    project_id = request.args['id']
    project = db.session.query(Project).filter_by(id=project_id).first()

    has_permissions = has_role('admin') or is_project_manager(project)
    users_list_body = []

    for user in project.users:    
        see_user = generate_action(user.id, 'user_details', 
            button_class='btn btn-outline-primary',
            text_class="fa-solid fa-eye",
            title="View user details")

        users_list_body.append({
            'data' : [user.id, user.first_name, user.last_name, user.job],
            'actions' : [see_user]
        })

    manager = db.session.query(User).filter_by(id=project.manager_id).first()
    if manager:
        project_manager = ' '.join([manager.first_name, manager.last_name])
    else:
        project_manager = None
 
    return render_template('projects/project_details.html',        
        context={
            'id' : project.id,
            'description' : project.description,
            'start_date' : project.start.strftime(f'%m-%d-%Y'),
            'finish_date' : project.finish.strftime(f'%m-%d-%Y'),
            'manager': project_manager,
            'has_permissions' : has_permissions,
            'available' : project.available,
            'generate_action' : generate_action
        },   
        list_context= {
                'list_header': users_projects_list_header,
                'list_body' : users_list_body
            })


@app.route('/projects/manage_project_users')
def manage_project():
    """Agregar o eliminar usuarios del proyecto """
    project = db.session.query(Project).filter_by(id=request.args['id']).first()
    error_happened = False
    if not has_role('admin') and not is_project_manager(project):
        error_happened = True
        
    users_projects_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'First name', 'class': 'col-6'},
        {'label': 'Last name', 'class': 'col-2'},
        {'label' : 'actions', 'class': 'col-1'} 
    ]
    mode = request.args['mode']
    project_id = request.args['id']
    project = db.session.query(Project).filter_by(id=project_id).first()

    if mode == 'Add':
        all_users = db.session.query(User).all()
        users = [user for user in all_users if user not in project.users]
    else:
        users = project.users
    
    users_list_body = []    
    for user in users:
        input_hidden = [{'name' : 'project_id', 'data' : project_id}]
        if mode == 'Edit_manager':
            button = generate_action(user.id, 'edit_manager', 'post',
                button_class='btn btn-outline-primary',
                text_class="fa-solid fa-check",
                title="Select as manager", hiddens=input_hidden)

        elif mode == 'Add':
            button = generate_action(user.id, 'add_user_to_project', 'post',
                button_class='btn btn-outline-primary',
                text_class="fa-solid fa-plus",
                title="Add user", hiddens=input_hidden)

        else:
            button = generate_action(user.id, 'remove_user_from_project', 'post', 
                button_class='btn btn-outline-danger',
                text_class="fa fa-trash",
                title="Remove user", hiddens=input_hidden)


        users_list_body.append({
            'data' : [user.id, user.first_name, user.last_name],
            'actions' : [button]
        })
    if error_happened:
        title = Errors(ERROR_MUST_BE_ADMIN_AND_MANAGER).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN_AND_MANAGER).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('projects_list'))
        
    return render_template('projects/manage_project_users.html',
        context={
            'id' : project.id,
            'mode' : mode,
        },   
        list_context= {
                'list_header': users_projects_list_header,
                'list_body' : users_list_body
            })


def adding_user_to_project(project_id,user_id):
    project = db.session.query(Project).filter_by(id=project_id).first()
    if not has_role('admin') and not is_project_manager(project):
        return False     
    
    user = db.session.query(User).filter_by(id=user_id).first()
    project.users.append(user)
    log = Logger('Adding user')

    db.session.add(log)
    
    db.session.commit()
    return project

@app.route('/projects/manage_project_users/add', methods=["POST"])
def add_user_to_project():
    "Agrega un usuario al proyecto"
    project_id = request.form['project_id']
    user_id = request.form['id']
    p = adding_user_to_project(project_id,user_id)
    if p == False:
        title = Errors(ERROR_MUST_BE_ADMIN_AND_MANAGER).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN_AND_MANAGER).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('projects_list')) 
    
    return redirect(url_for('manage_project', mode='Add', id=request.form['project_id']))

def removing_user_from_project(project_id,user_id):
    project = db.session.query(Project).filter_by(id=project_id).first()
    if not has_role('admin') and not is_project_manager(project):
        return False

    user = db.session.query(User).filter_by(id=user_id).first()
    log = Logger('Deleting user')
    project.users.remove(user)
    db.session.add(log)
    db.session.commit()
    return project


@app.route('/projects/manage_project_users/remove',  methods=["POST"])
def remove_user_from_project():
    "Elimina un usuario del proyecto"
    project_id = request.form['project_id']
    user_id = request.form['id']
    p = removing_user_from_project(project_id,user_id)
    if p == False:
        title = Errors(ERROR_MUST_BE_ADMIN_AND_MANAGER).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN_AND_MANAGER).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('projects_list')) 
    
    return redirect(url_for('manage_project', mode='Remove', id=request.form['project_id']))


def editing_manager(project_id,manager_id):
    project = db.session.query(Project).filter_by(id=project_id).first()

    if not has_role('admin') and not is_project_manager(project):
        return False

    project.manager_id = manager_id

    db.session.commit()
    return project

@app.route('/projects/manage_project_users/select_manager',  methods=["POST"])
def edit_manager():
    "Selecciona el gerente para el proyecto"

    project_id = request.form['project_id']
    manager_id = request.form['id']
    p = editing_manager(project_id,manager_id)
    if p == False:
        title = Errors(ERROR_MUST_BE_ADMIN_AND_MANAGER).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN_AND_MANAGER).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('project_details', id=request.form['project_id']))

    return redirect(url_for('project_details', id=request.form['project_id']))
    

def removing_manager(project_id):
    project = db.session.query(Project).filter_by(id=project_id).first()
    if not has_role('admin') and not is_project_manager(project):
        return False

    project.manager_id = None

    db.session.commit()
    return project


@app.route('/projects/manage_project_users/remove_manager')
def remove_manager():
    "Elimina el gerente actual para el proyecto"

    project_id = request.args['id']
    p = removing_manager(project_id)
    if p == False:
        title = Errors(ERROR_MUST_BE_ADMIN_AND_MANAGER).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN_AND_MANAGER).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('project_details')) 
    
    return redirect(url_for('project_details', id=request.args['id']))
