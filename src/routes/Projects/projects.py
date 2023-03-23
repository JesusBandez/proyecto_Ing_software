from flask import after_this_request, render_template, request, send_file, session, redirect, url_for, flash, send_from_directory,jsonify
from src.lib.generate_action import generate_action
from src.routes.auth import has_role
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
    users_list_header = [
        {'label': 'Id', 'class': 'col'},
        {'label': 'Car', 'class': 'col'},
        {'label': 'Department', 'class': 'col'},
        {'label': 'Manager', 'class': 'col'},
        {'label': 'Issue', 'class': 'col'},
        {'label': 'Solution', 'class': 'col'}, 
        {'label': 'Amount ($)', 'class': 'col'},
        {'label': 'Observations', 'class': 'col'},            
        {'label': 'Actions', 'class': 'col'},        
    ]
    try:
        typeS = request.form['typeSearch']
        search = request.form['search']
        PROJECTS = search_projects(typeS,search)
        if PROJECTS.count() == 0:
            PROJECTS = db.session.query(Project).all()
    except:
        PROJECTS = db.session.query(Project).all()

    projects_list_body = []
    for project in PROJECTS:
    
        generate = generate_action(project.id,
            'generate_project', button_class='btn btn-outline-primary',
            text_class='fa-regular fa-rectangle-list',
            title="Project Details")
        
        remove = generate_action(project.id, 'remove_project', 'post',
            button_class='btn btn-outline-danger',
            title="Remove project",
            text_class='fa-solid fa-trash',
            disabled= not has_role('admin'))

        budget_project = generate_action(project.id,            
            'print_project', 'post',
            text_class='fa-solid fa-sack-dollar',
            title="Project Budget",
            button_class='btn btn-outline-success', 
            disabled = not has_role('user'))

        if project.manager:
            manager_name = project.manager.first_name +" "+ project.manager.last_name
        else:
            manager_name = 'Without manager'
        
        
        projects_list_body.append({
            'data' : [project.id, project.car, project.department, manager_name,
                    project.issue, project.solution, project.amount, project.observations],
            'actions' : [generate, budget_project, remove]
            })
     

    return render_template('projects/projects.html',
        has_role=has_role,
        list_context= {
                'list_header': users_list_header,
                'list_body' : projects_list_body
            })

# Agregar proyectos
@app.route('/projects/new_project')
def new_project():
    if not has_role('admin'):
        title = Errors(ERROR_MUST_BE_ADMIN).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('projects_list'))    
    "Muestra el formulario para agregar o editar un proyecto"
    department = db.session.query(Department).all()
    return render_template('projects/new_project.html', project_to_edit=None, all_departments = department)


def adding_new_project(id_project_to_edit, description, start_date, close_date,car,department,
        manager,issue,solution,amount,obs):
    project_car = db.session.query(Car).filter_by(license_plate=car).first()
    m = manager.split(" ")
    project_manager = db.session.query(User).filter_by(id=int(m[0])).first()

    if not id_project_to_edit:
        project = Project(description, start_date, close_date,project_car.license_plate,department,
            issue,solution,obs, project_manager.id, amount)
        log = Logger('Adding project')
        db.session.add_all([log, project])        
        db.session.flush()
        db.session.refresh(project)
        
    else:        
        changes = {
            'description' : description,
            'start' : start_date,
            'finish' : close_date,  
            'car' : project_car.license_plate,
            'department' : department,
            'issue' : issue,
            'solution' : solution,
            'observations' : obs,
            'manager_id' : project_manager.id,
            'amount' : amount        
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
def add_new_project():
    """Obtiene los datos para agregar un nuevo proyecto y 
        lo agrega al sistema"""
    if not has_role('admin'):
        title = Errors(ERROR_MUST_BE_ADMIN).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('projects_list'))
    id_project_to_edit = request.form.get('id_project')
    description = request.form['description']
    car = request.form['car_selection'] #la placa
    department = request.form['department']  #la descripcion
    manager = request.form['manager_selection'] #id nombre apellido
    issue = request.form['issue']
    solution = request.form['solution']
    amount = request.form['amount']
    obs = request.form['observation']
    start_date = datetime.strptime(request.form['s_date'], r'%Y-%m-%d')
    close_date = datetime.strptime(request.form['c_date'], r'%Y-%m-%d')
    
    project = adding_new_project(id_project_to_edit, description, start_date, close_date,car,department,
        manager,issue,solution,amount,obs)
            
    return redirect(url_for('project_details', id=project.id))


@app.route('/projects/list/generate_project', methods=['GET', 'POST'])
def generate_project():
    "Generar proyecto"
    # TODO: No se que hace esta vaina pero la voy a usar para los detalles
    print("Generando")
    return redirect(url_for('project_details', id=request.args['id']))

@app.route('/projects/list/edit_project', methods=['POST'])
def edit_project():
    #"Editar proyecto"
    if not has_role('admin'):
        title = Errors(ERROR_MUST_BE_ADMIN).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('projects_list'))
    project = db.session.query(Project).filter_by(
        id=request.form['id']).first()
    edit_context = {
        'id' : project.id,
        'description': project.description,
        'start' : project.start.date(),
        'finish' : project.finish.date(),
        'users' : project.users
    }
    return render_template('projects/new_project.html', project_to_edit=edit_context)

def removing_project(project_id):
    project = db.session.query(Project).filter_by(id=project_id).first()

    log = Logger('Editing project')

    db.session.add(log)
    db.session.delete(project)
    db.session.commit()
    return project


@app.route('/projects/list/remove_project', methods=['GET', 'POST'])
def remove_project():
    "Eliminar proyecto"
    if not has_role('admin'):
        title = Errors(ERROR_MUST_BE_ADMIN).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('projects_list'))
        
    project_id = request.form['id']

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
    if not has_role('admin'):
        title = Errors(ERROR_MUST_BE_ADMIN).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('projects_list'))

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
    show_project = {
        'id' : project.id,
        'description' : project.description,
        'start_date' : project.start.strftime(f'%m-%d-%Y'),
        'finish_date' : project.finish.strftime(f'%m-%d-%Y')
    }
    
    users_list_body = []
    for user in project.users:
        users_list_body.append({
            'data' : [user.id, user.first_name, user.last_name, user.job]
        })

    rendered = render_template('print_project/print_project.html',
                               context=show_project,
                               list_context= {
                                    'list_header': users_projects_list_header,
                                    'list_body' : users_list_body
                                })
    
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
