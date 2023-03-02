from flask import render_template, request, session, redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.routes.auth import has_role
from src.models import db
from src.models.Project import Project
from src.models.User import User
from src.models.Logger import Logger
from datetime import datetime
from . import app


@app.route('/projects/project_details')
def project_details():
    """Renderiza la vista con la lista de proyectos de un usuario.
        El Id del usuario se obtiene por url args"""
    
    users_projects_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'First name', 'class': 'col-3'},
        {'label': 'Last name', 'class': 'col-3'},
        {'label' : 'job', 'class' : 'col-3'},
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
            'data' : [user.id, user.first_name, user.last_name, user.job],
            'actions' : [see_user]
        })

    manager = db.session.query(User).filter_by(id=project.manager_id).first()
    if manager:
        project_manager = ' '.join([manager.first_name, manager.last_name])
    else:
        project_manager = 'None'
    
    return render_template('projects/project_details.html',
        has_role=has_role,
        context={
            'id' : project.id,
            'description' : project.description,
            'start_date' : project.start.strftime(f'%m-%d-%Y'),
            'finish_date' : project.finish.strftime(f'%m-%d-%Y'),
            'manager': project_manager,
        },   
        list_context= {
                'list_header': users_projects_list_header,
                'list_body' : users_list_body
            })


@app.route('/projects/manage_project_users')
def manage_project():
    """Agregar o eliminar usuarios del proyecto """
    if not has_role('admin'):
        return redirect(url_for('projects_list'))

    users_projects_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'First name', 'class': 'col-6'},
        {'label': 'Last name', 'class': 'col-2'},
        {'label' : 'actions', 'class': 'col-1'} 
    ]
    mode = request.args['mode']
    project_id = request.args['id']
    project = db.session.query(Project).filter_by(id=project_id).first()

    if mode == 'Edit_manager':
        users = db.session.query(User).all()
    elif mode == 'Add':
        all_users = db.session.query(User).all()
        users = [user for user in all_users if user not in project.users]
    else:
        users = project.users
    
    users_list_body = []    
    for user in users:
        input_hidden = [{'name' : 'project_id', 'data' : project_id}]
        if mode == 'Edit_manager':
            button = generate_action(user.id, 'edit_manager', 'post',
                button_class='btn btn-info w-100',
                text_class="fa-solid fa-check",
                title="Select as manager", hiddens=input_hidden)

        elif mode == 'Add':
            button = generate_action(user.id, 'add_user_to_project', 'post',
                button_class='btn btn-info w-100',
                text_class="fa-solid fa-plus",
                title="Add user", hiddens=input_hidden)

        else:
            button = generate_action(user.id, 'remove_user_from_project', 'post', 
                button_class='btn btn-danger w-100',
                text_class="fa fa-trash",
                title="Remove user", hiddens=input_hidden)


        users_list_body.append({
            'data' : [user.id, user.first_name, user.last_name],
            'actions' : [button]
        })

    return render_template('projects/manage_project_users.html',
        has_role=has_role,
        context={
            'id' : project.id,
            'mode' : mode,
        },   
        list_context= {
                'list_header': users_projects_list_header,
                'list_body' : users_list_body
            })

@app.route('/projects/manage_project_users/add', methods=["POST"])
def add_user_to_project():
    "Agrega un usuario al proyecto"
    if not has_role('admin'):
        return redirect(url_for('projects_list'))
        
    project = db.session.query(Project).filter_by(id=request.form['project_id']).first()
    user = db.session.query(User).filter_by(id=request.form['id']).first()
    project.users.append(user)
    time_data = datetime.now()
    date = time_data.strptime(time_data.strftime(r'%Y-%m-%d'), r'%Y-%m-%d')
    hour = time_data.strptime(time_data.strftime(r'%H:%M:%S'), r'%H:%M:%S')
    log = Logger('Adding user', date, hour)

    db.session.add(log)
    db.session.commit()
    return redirect(url_for('manage_project', mode='Add', id=request.form['project_id']))

@app.route('/projects/manage_project_users/remove',  methods=["POST"])
def remove_user_from_project():
    "Elimina un usuario del proyecto"
    if not has_role('admin'):
        return redirect(url_for('projects_list'))

    project = db.session.query(Project).filter_by(id=request.form['project_id']).first()
    user = db.session.query(User).filter_by(id=request.form['id']).first()
    time_data = datetime.now()
    date = time_data.strptime(time_data.strftime(r'%Y-%m-%d'), r'%Y-%m-%d')
    hour = time_data.strptime(time_data.strftime(r'%H:%M:%S'), r'%H:%M:%S')
    log = Logger('Deleting user', date, hour)

    db.session.add(log)
    project.users.remove(user)
    db.session.commit()
    return redirect(url_for('manage_project', mode='Remove', id=request.form['project_id']))

@app.route('/projects/manage_project_users/select_manager',  methods=["POST"])
def edit_manager():
    "Selecciona el gerente para el proyecto"
    if not has_role('admin'):
        return redirect(url_for('projects_list'))
    project = db.session.query(Project).filter_by(id=request.form['project_id']).first()    
    project.manager_id = request.form['id']

    db.session.commit()
    return redirect(url_for('project_details', id=request.form['project_id']))