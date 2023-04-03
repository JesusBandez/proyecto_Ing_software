from flask import session, flash, redirect, url_for, request
from src.models import db

from functools import wraps
from src.errors import Errors, ERROR_MUST_BE_ADMIN, ERROR_MUST_BE_ADMIN_AND_MANAGER,ERROR_MUST_BE_ADMIN_DELETE_USER, ERROR_MUST_BE_ADMIN_NEW_USER, ERROR_MUST_BE_ADMIN_ADD_DEPARTMENT,ERROR_MUST_BE_ADMIN_DELETE_DEPARTMENT,ERROR_MUST_BE_ADMIN_ADD_CLIENT,ERROR_EXISTS_LICENSE_PLATE,ERROR_MUST_BE_ADMIN_DELETE_CLIENT
from src.models.Project import Project


USER_ROLE = 'user'
ADMIN_ROLE = 'admin'
OPERATIONS_ANALYST = 'opera'
MANAGER = 'mger'
PROJECT_MANAGER = 'pmger'
MECHANICS_MANAGER = 'mech'
STRUCTURE_MANAGER = 'strct'
PAINT_MANAGER = 'paint'
ELECTRONIC_MANAGER = 'elect'
ELECTRICITY_MANAGER = 'electric'
MECHANIC_SPECIALIST = 'mechs'
STRUCTURE_SPECIALIST = 'strcts'
PAINT_SPECIALIST = 'paints'
ELECTRONIC_SPECIALIST = 'elects'
ELECTRICITY_SPECIALIST = 'electrics'

ROLES = [USER_ROLE,ADMIN_ROLE,OPERATIONS_ANALYST,MANAGER,PROJECT_MANAGER,MECHANICS_MANAGER,STRUCTURE_MANAGER,PAINT_MANAGER,
ELECTRONIC_MANAGER,ELECTRICITY_MANAGER,MECHANIC_SPECIALIST,STRUCTURE_SPECIALIST,PAINT_SPECIALIST,
ELECTRONIC_SPECIALIST,ELECTRICITY_SPECIALIST]


def error_display(error_type):
    title = Errors(error_type).error.title
    desc = Errors(error_type).error.description
    flash(True, 'error')
    flash(title, 'error_title') 
    flash(desc, 'error_description')

def require_permissions(func):
    @wraps(func)
    def inner1(*args, **kwargs):
        name = func.__name__
        if (not has_role('admin') and not has_role('mngr')) and (name=="new_project" or name=="add_new_project" or name=="remove_project" or 
            name == "toggle_project_availability"):
            error_display(ERROR_MUST_BE_ADMIN)
            return redirect(url_for('projects_list'))
        if name == "manage_project":
            project = db.session.query(Project).filter_by(id=request.args['id']).first()
            mode = request.args['mode'] #Aqui se puede agarrar el modo de manage project
            if not has_role('admin') and not has_role('mngr') and not is_project_manager(project):
                error_display(ERROR_MUST_BE_ADMIN_AND_MANAGER)
                return redirect(url_for('projects_list'))

        if name == "delete_user" and not has_role('admin'):
            error_display(ERROR_MUST_BE_ADMIN_DELETE_USER)
            return redirect(url_for('users_lists'))
        if name == "new_user" and not has_role('admin'):
            error_display(ERROR_MUST_BE_ADMIN_NEW_USER)
            return redirect(url_for('users_lists'))
        if name == "new_department" and not has_role('admin'):
            error_display(ERROR_MUST_BE_ADMIN_ADD_DEPARTMENT)
            return redirect(url_for('departments_list'))
        if name == "add_new_department" and not has_role('admin'):
            error_display(ERROR_MUST_BE_ADMIN)
            return redirect(url_for('departments_list'))
        if name == "remove_department" and not has_role('admin'):
            error_display(ERROR_MUST_BE_ADMIN_DELETE_DEPARTMENT)
            return redirect(url_for('departments_list'))

        if name == "new_client" and not has_role('opera'):
            error_display(ERROR_MUST_BE_ADMIN_ADD_CLIENT)
            return redirect(url_for('clients_list'))
        if name== "new_car" and not has_role('opera'):
            owner_id = request.form['owner_id']
            error_display(ERROR_MUST_BE_ADMIN)
            return redirect(url_for('client_details',id=owner_id))
        if name == "remove_car" and not has_role('opera'):
            owner_id = request.form['owner_id']
            error_display(ERROR_MUST_BE_ADMIN)
            return redirect(url_for('client_details',id=owner_id))
        if name == "remove_client" and not has_role('opera'):
            error_display(ERROR_MUST_BE_ADMIN_DELETE_CLIENT)
            return redirect(url_for('clients_list'))

        #Funciones que retornan False para unit tests y tambien verifican si tiene o no un rol especifico
        if (name=="adding_client" or name=="removing_client" or name=="removing_car") and not has_role('opera'):
            return False
        if name=="adding_user_to_project" or name=="removing_user_from_project":
            project = db.session.query(Project).filter_by(id=args[0]).first()
            if not has_role('admin') and not is_project_manager(project):
                return False


        returned_value = func(*args, **kwargs)
        return returned_value
         
    return inner1


def has_role(role='user'):
    '''Comprueba si un usuario tiene un determinado rol de permisos
    role : Rol que se comprueba que el usuario cumple
    El rol del usuario logeado se encuentra en session['user']['role'] 
    '''

    if not session.get('user'):
        return False

    if role == 'user':
        return session.get('user')['role'] in ['user', 'opera', 'admin']

    elif role == 'opera':
        return session.get('user')['role'] in ['opera', 'admin']

    elif role == 'mngr':
        return session.get('user')['role'] == 'mngr'

    elif role == 'admin':
        return session.get('user')['role'] == 'admin'

    raise Exception(f'Rol: {role} no reconocido')

def is_project_manager(project):
    '''Comprueba si el usuario logeado es el manager del proyecto. 
    Retorna False si el proyecto no tiene manager'''
    if not session.get('user'):
        return False

    return project.manager_id != None and session['user']['id'] == project.manager_id
    
