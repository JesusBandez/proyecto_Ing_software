from flask import after_this_request, render_template, request, send_file, session, redirect, url_for, flash, send_from_directory,jsonify
from src.lib.generate_action import generate_action
from src.lib.class_create_button import ListProjects
from src.lib.class_create_button import ListProjectsUser, ListActionPlansList
from src.routes.auth import has_role, is_project_manager, require_permissions
from src.routes.Projects import project_details
from src.models import db
from src.models.Project import Project
from src.models.User import User
from src.models.Logger import Logger

from src.models.Client import Client
from src.models.Car import Car
from src.models.Department import Department

from datetime import datetime
from sqlalchemy import extract,or_

from src.errors import Errors, ERROR_MUST_BE_ADMIN, ERROR_MUST_BE_ADMIN_AND_MANAGER

import pdfkit
import os
from . import app


@app.route("/ajaxlivesearchmanager",methods=["POST","GET"])
def ajaxlivesearchmanager():
    if request.method == 'POST':
        search_word = request.form['search']

        if search_word != '':
            users = db.session.query(User).filter(or_(User.first_name.contains(search_word),User.last_name.contains(search_word))).all()
        else:
            users = db.session.query(User).all()
    return jsonify({'htmlresponse': render_template('projects/table_for_project.html', all_info=users, count=1)})
     

@app.route("/ajaxlivesearch",methods=["POST","GET"])
def ajaxlivesearch():
    if request.method == 'POST':
        search_word = request.form['search']

        if search_word != '':
            cars = db.session.query(Car).filter(Car.license_plate.contains(search_word)).all()
        else:
            cars = db.session.query(Car).all()
        all_info = []
        for car in cars:
            o = db.session.query(Client).filter_by(id=car.owner).first()
            all_info.append([car,o])
    return jsonify({'htmlresponse': render_template('projects/table_for_project.html', all_info=all_info, count=0)})
     

def search_projects(typeS,search):
    if typeS == "des":
        projects = db.session.query(Project).filter(Project.description.contains(search))
    elif typeS == "start":
        projects = db.session.query(Project).filter(extract('month', Project.start)==int(search))
    elif typeS == "finish":
        projects = db.session.query(Project).filter(extract('month', Project.finish)==int(search))
    elif typeS == "id":
        projects = db.session.query(Project).filter(Project.id.ilike(search))
    else:
        projects = db.session.query(Project).all()
    return projects

# Proyectos del sistema
@app.route('/projects/list', methods=('GET', 'POST'))
def projects_list():
    "Renderiza la lista con todos los proyectos del sistema"
    try:
        typeS = request.form['typeSearch']
        search = request.form['search']
        PROJECTS = search_projects(typeS,search)
        if PROJECTS.count() == 0:
            PROJECTS = db.session.query(Project).all()
    except:
        PROJECTS = db.session.query(Project).all()

    A = ListProjects(PROJECTS)
    projects_list_body = A.list_table()
    users_list_header = A.header

    return render_template('projects/projects.html',
        has_role=has_role,
        list_context= {
                'list_header': users_list_header,
                'list_body' : projects_list_body
            })

# Agregar proyectos
@app.route('/projects/new_project', methods=['POST', 'GET'])
@require_permissions
def new_project():
    "Muestra el formulario para agregar o editar un proyecto"
    department = db.session.query(Department).all()

    project, manager = None, None
    if request.form.get('id'):
        project = db.session.query(Project).filter_by(
            id=request.form.get('id')).first()
        
        if project.manager_id:
            manager = db.session.query(User).filter_by(id=project.manager_id).first()
            manager = ' '.join([str(manager.id), manager.first_name,  manager.last_name])

    return render_template('projects/new_project.html', project_to_edit=project, 
        all_departments = department, manager=manager)

def adding_new_project(id_project_to_edit, description, start_date, close_date,car,department,
        manager,issue,solution,obs):
    
    manager_id = int(manager.split(" ")[0])  

    if not id_project_to_edit:
        project = Project(description, start_date, close_date,car,department,
            issue,solution,obs, manager_id)
        log = Logger('Adding project')
        db.session.add_all([log, project])        
        db.session.flush()
        db.session.refresh(project)
        
    else:        
        changes = {
            'description' : description,
            'start' : start_date,
            'finish' : close_date,  
            'car' : car,
            'department' : department,
            'issue' : issue,
            'solution' : solution,
            'observations' : obs,
            'manager_id' : manager_id,      
            }
        db.session.query(Project).filter_by(
            id=id_project_to_edit).update(changes)
        project = db.session.query(Project).filter_by(
            id=id_project_to_edit).first()
        log = Logger('Editing project')
        
            
    db.session.add(log)        
    db.session.commit()
    return project


@app.route('/projects/new_project/add', methods=['POST'])
@require_permissions
def add_new_project():
    """Obtiene los datos para agregar un nuevo proyecto y 
        lo agrega al sistema"""
    
    id_project_to_edit = request.form.get('id_project')
    description = request.form['description']
    car = request.form['car_selection'] #la placa
    department = request.form['department']
    manager = request.form['manager_selection'] #id nombre apellido
    issue = request.form['issue']
    solution = request.form['solution']    
    obs = request.form['observation']
    start_date = datetime.strptime(request.form['s_date'], r'%Y-%m-%d')
    close_date = datetime.strptime(request.form['c_date'], r'%Y-%m-%d')
    
    project = adding_new_project(id_project_to_edit, description, start_date, close_date,car,department,
        manager,issue,solution,obs)
            
    return redirect(url_for('project_details', id=project.id))


@app.route('/projects/list/generate_project', methods=['GET', 'POST'])
def generate_project():
    "Generar proyecto"

    return redirect(url_for('project_details', id=request.args['id']))

@app.route('/projects/list/project_budget', methods=['GET', 'POST'])
def project_budget():
    "Presupesto del proyecto"   

    return redirect(f"{url_for('project_details', id=request.args['id'])}#actionplan")

def removing_project(project_id):
    project = db.session.query(Project).filter_by(id=project_id).first()

    log = Logger('Editing project')
    for plan in project.action_plans:
        db.session.delete(plan)

    db.session.add(log)
    db.session.delete(project)
    db.session.commit()
    return project


@app.route('/projects/list/remove_project', methods=['GET', 'POST'])
def remove_project():
    "Eliminar proyecto"
        
    project_id = request.args['id']                         
    removing_project(project_id)
    
    return redirect(url_for('projects_list'))


def change_availability(project_id):
    project = db.session.query(Project).filter_by(id=project_id).first()
    project.available = not project.available
    db.session.commit()
    return project

@app.route('/projects/list/toggle_project_availability', methods=['POST'])
def toggle_project_availability():
    "Habilitar/desabilitar proyecto"

    change_availability(request.form['id'])
    
    return redirect(url_for('project_details', id=request.form['id']))

@app.route('/projects/print_project', methods=['POST'])
def print_project():
    users_projects_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'First name', 'class': 'col-3'},
        {'label': 'Last name', 'class': 'col-3'},
        {'label' : 'job', 'class' : 'col-3'}
    ]
    project_id = request.form['id']
    project = db.session.query(Project).filter_by(id=project_id).first()
    
    users_list_body = []
    for user in project.users:
        users_list_body.append({
            'data' : [user.id, user.first_name, user.last_name, user.job]
        })
    
    has_permissions = has_role('admin') or is_project_manager(project)
    
    manager = db.session.query(User).filter_by(id=project.manager_id).first()
    if manager:
        project_manager = ' '.join([manager.first_name, manager.last_name])
    else:
        project_manager = 'Without manager assigned'

    car_plate = project.car if project.car else 'N/A'

    department_description = (
        project.associated_department.description if project.associated_department else 'N/A')
    action_plans = project.action_plans
    list_action_plans = ListActionPlansList(action_plans, project_id)

    rendered = render_template('projects/project_details.html',
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
            'amount' : str(project.amount)+'$',
            'has_permissions' : has_permissions,
            'available' : project.available,
            'generate_action' : generate_action
        },   
        users_list_context= {
                'list_header': users_projects_list_header,
                'list_body' : users_list_body
            },
        actions_plans_list_context = {
                'list_header': list_action_plans.header,
                'list_body' : list_action_plans.list_table()
        }    
            ) 
    
    if (os.name == 'nt') :
        pathToWkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=pathToWkhtmltopdf)
        pdfkit.from_string(rendered, f'.\printed\{project_id}.pdf', configuration=config)
    else :
        pdfkit.from_string(rendered, f'./printed/{project_id}.pdf')

    log = Logger('Printing project')
    db.session.add(log)
    db.session.commit()   

    @after_this_request
    def remove_file(response):
        if (os.name == 'nt') :
            # os.remove(f'.\printed\{project_id}.pdf')
            pass
        else:
            os.remove(f'./printed/{project_id}.pdf')
        return response

    return send_file(f'./printed/{project_id}.pdf', as_attachment=True)
