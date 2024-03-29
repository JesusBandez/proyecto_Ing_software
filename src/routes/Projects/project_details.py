from flask import render_template, request, session, redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.lib.class_create_button import ListProjectsUser, ListManageProjectUsers, ListActionPlansList

from src.routes.auth import has_role, is_project_manager, require_permissions
from src.models import db
from src.models.Project import Project
from src.models.User import User
from src.models.Logger import Logger
from src.models.ActionPlan import ActionPlan
from datetime import datetime

from src.errors import Errors, ERROR_MUST_BE_ADMIN, ERROR_MUST_BE_ADMIN_AND_MANAGER
from . import app


def searchActionPlan(typeS,search,project_id):
    if typeS == "activity":
        plan = db.session.query(ActionPlan).filter(ActionPlan.project == project_id, ActionPlan.activity.contains(search))
    elif typeS == "action":
        plan = db.session.query(ActionPlan).filter(ActionPlan.project == project_id, ActionPlan.action.contains(search))
    elif typeS == "responsible":
        user = db.session.query(User).filter((User.first_name + User.last_name).contains(search)).first()
        plan = db.session.query(ActionPlan).filter(ActionPlan.project == project_id, ActionPlan.responsible.contains(user.id))
    return plan


@app.route('/projects/project_details', methods=('GET', 'POST'))
def project_details():
    """Renderiza la vista con la lista de proyectos de un usuario.
        El Id del usuario se obtiene por url args"""

    project_id = request.args['id']
    project = db.session.query(Project).filter_by(id=project_id).first()

    has_permissions = has_role('mngr') or has_role('admin') or is_project_manager(project)

    manager = db.session.query(User).filter_by(id=project.manager_id).first()
    if manager:
        project_manager = ' '.join([manager.first_name, manager.last_name])
    else:
        project_manager = 'Without manager assigned'

    car_plate = project.car if project.car else 'N/A'

    department_description = (
        project.associated_department.description if project.associated_department else 'N/A')
    
    try:
        typeS = request.form['typeSearch']
        search = request.form['search']
        action_plans = searchActionPlan(typeS,search,project_id)
        if action_plans.count() == 0:
            action_plans = project.action_plans
    except:
        action_plans = project.action_plans
    list_project_users = ListProjectsUser(project.users)
    list_action_plans = ListActionPlansList(action_plans, project_id)


    return render_template('projects/project_details.html',
        has_role=has_role,      
        context={
            'id' : project.id,
            'description' : project.description,
            'start_date' : project.start.strftime(f'%m-%d-%Y'),
            'finish_date' : project.finish.strftime(f'%m-%d-%Y'),
            'manager': project_manager,
            'car_plate': car_plate,
            'department' : department_description,
            'issue' : project.issue,
            'solution' : project.solution,
            'observations' : project.observations,
            'amount' : f'{project.project_cost()}$',
            'has_permissions' : has_permissions,
            'available' : project.available,
            'generate_action' : generate_action,
            'is_project_manager' : is_project_manager(project)
            },   
        users_list_context= {
                'list_header': list_project_users.header,
                'list_body' : list_project_users.list_table()
            },
        actions_plans_list_context = {
                'list_header': list_action_plans.header,
                'list_body' : list_action_plans.list_table()
        }
            )


@app.route('/projects/manage_project_users')
@require_permissions
def manage_project():
    """Agregar o eliminar usuarios del proyecto """
    project = db.session.query(Project).filter_by(id=request.args['id']).first()
        
    mode = request.args['mode']
    project_id = request.args['id']
    project = db.session.query(Project).filter_by(id=project_id).first()

    if mode == 'Add':
        all_users = db.session.query(User).all()
        users = [user for user in all_users if user not in project.users]
    else:
        users = project.users

    A = ListManageProjectUsers(users,mode,project)
    A.button_to_create()
    users_list_body = A.list_table()
    users_projects_list_header = A.header
        
    return render_template('projects/manage_project_users.html',
        context={
            'id' : project.id,
            'mode' : mode,
        },   
        list_context= {
                'list_header': users_projects_list_header,
                'list_body' : users_list_body
            })

@require_permissions
def adding_user_to_project(project_id,user_id):
    project = db.session.query(Project).filter_by(id=project_id).first()     
    
    user = db.session.query(User).filter_by(id=user_id).first()
    project.users.append(user)
    log = Logger('Adding user')

    db.session.add(log)
    
    db.session.commit()
    return project

@app.route('/projects/manage_project_users/add', methods=["POST"])
@require_permissions
def add_user_to_project():
    "Agrega un usuario al proyecto"
    project_id = request.form['project_id']
    user_id = request.form['id']
    p = adding_user_to_project(project_id,user_id)
    
    return redirect(url_for('manage_project', mode='Add', id=request.form['project_id']))

@require_permissions
def removing_user_from_project(project_id,user_id):
    project = db.session.query(Project).filter_by(id=project_id).first()
    
    user = db.session.query(User).filter_by(id=user_id).first()
    log = Logger('Deleting user')
    project.users.remove(user)
    db.session.add(log)
    db.session.commit()
    return project


@app.route('/projects/manage_project_users/remove',  methods=["POST"])
@require_permissions
def remove_user_from_project():
    "Elimina un usuario del proyecto"
    project_id = request.form['project_id']
    user_id = request.form['id']
    p = removing_user_from_project(project_id,user_id)
    
    return redirect(url_for('manage_project', mode='Remove', id=request.form['project_id']))
