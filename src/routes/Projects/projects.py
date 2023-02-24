from flask import render_template, request, session, redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.routes.auth import has_role
from src.models import db
from src.models.Project import Project
from src.models.User import User
from datetime import datetime
import pdfkit
from . import app


# Proyectos del sistema
@app.route('/projects/list', methods=('GET', 'POST'))
def projects_list():
    "Renderiza la lista con todos los proyectos del sistema"

    users_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'Description', 'class': 'col-3'},
        {'label': 'Start', 'class': 'col-2'},
        {'label': 'End', 'class': 'col-2'},
        {'label': 'Users in project', 'class': 'col-3'},
        {'label': 'Actions', 'class': 'col-4'},        
    ]

    # TODO: Obtener los proyectos de la base de datos y arreglar
    # el codigo de debajo

    PROJECTS = db.session.query(Project).all()
    projects_list_body = []
    for project in PROJECTS:
    
        generate = generate_action(project.id,
            'generate_project', button_class='btn btn-sm btn-info w-100',
            text_class='fa-regular fa-rectangle-list',
            title="Generate project",
            disabled=not project.available)

        # ready
        edit = generate_action(project.id,
            'edit_project', method='post', 
            button_class='btn btn-sm btn-info w-100',
            title="Edit project",
            text_class='fa-solid fa-pencil',
            disabled=not project.available)

        # ready
        remove = generate_action(project.id, 'remove_project', 'post',
            button_class='btn btn-sm btn-danger w-100',
            title="Remove project",
            text_class='fa-solid fa-trash',
            disabled=not has_role('admin'))

        # ready
        toggle_availability = generate_action(project.id,
            'toggle_project_availability', method='post',
            text_class= 'fa-solid fa-ban' if project.available else 'fa-solid fa-play',
            title="Disable project" if project.available else "Enable project",
            button_class='btn btn-sm btn-info w-100')

        # semi-ready
        print_project = generate_action(project.id,            
            'print_project', 'post',
            text_class='fa-solid fa-print',
            title="Print project",
            button_class='btn btn-sm btn-info w-100')

        
        projects_list_body.append({
            'data' : [project.id, project.description, 
                    project.start.strftime(f'%m-%d-%Y'), project.finish.strftime(f'%m-%d-%Y'), project.users],
            'actions' : [generate, edit, toggle_availability, print_project, remove]
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
    "Muestra el formulario para agregar o editar un proyecto"
    return render_template('projects/new_project.html', 
        project_to_edit=None)

@app.route('/projects/new_project/add', methods=['POST'])
def add_new_project():
    """Obtiene los datos para agregar un nuevo proyecto y 
        lo agrega al sistema"""

    id_project_to_edit = request.form.get('id_project')
    description = request.form['description']
    start_date = datetime.strptime(request.form['s_date'], r'%Y-%m-%d')
    close_date = datetime.strptime(request.form['c_date'], r'%Y-%m-%d')
    project_users = request.form['p_users']
    project_users = project_users.split(", ")
    
    if not id_project_to_edit:
        project = Project(description, start_date, close_date)
        for pu in project_users:
            user = db.session.query(User).filter_by(username=pu).first()
            if (user != None):
                project.users.append(user)
        db.session.add(project)
        db.session.commit()

    else:
        print(f"A editar {id_project_to_edit}")
        changes = {
            'description' : description,
            'start' : start_date,
            'finish' : close_date,
            'users' : project_users
            }
        project = db.session.query(Project).filter_by(
            id=id_project_to_edit).update(changes)
        db.session.commit()
                
    return redirect(url_for('projects_list'))


@app.route('/projects/list/generate_project', methods=['GET', 'POST'])
def generate_project():
    "Generar proyecto"
    # TODO: No se que hace esta vaina
    print("Generando")
    return redirect(url_for('projects_list'))

@app.route('/projects/list/edit_project', methods=['POST'])
def edit_project():
    "Editar proyecto"
    project = db.session.query(Project).filter_by(
        id=request.form['id']).first()
    edit_context = {
        'id' : project.id,
        'description': project.description,
        'start' : project.start.date(),
        'finish' : project.finish.date(),
        'users' : project.users
    }
    return render_template('projects/new_project.html', 
        project_to_edit=edit_context)

@app.route('/projects/list/remove_project', methods=['GET', 'POST'])
def remove_project():
    "Eliminar proyecto"
    if not has_role('admin'):
        return redirect(url_for('projects_lists'))
        
    project_id = request.form['id']
    project = db.session.query(Project).filter_by(id=project_id).first()

    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('projects_list'))

@app.route('/projects/list/toggle_project_availability', methods=['POST'])
def toggle_project_availability():
    "Habilitar/desabilitar proyecto"
    project = db.session.query(Project).filter_by(
            id=request.form['id']).first()
    project.available = not project.available
    db.session.commit()
    return redirect(url_for('projects_list'))

@app.route('/projects/list/print_project', methods=['GET', 'POST'])
def print_project():
    "Imprimir proyecto"
    project_id = request.form['id']
    project = db.session.query(Project).filter_by(id=project_id).first()
    string_to_print = ''
    string_to_print += 'Data for project ' + str(project.id) + '\n'
    string_to_print += 'Description: ' + project.description + '\n'
    string_to_print += 'Start date: ' + str(project.start.date()) + '\n'
    string_to_print += 'Finish date: ' + str(project.finish.date()) + '\n'
    string_to_print += 'Users working in project: ' + str(project.users)
    
    pdfkit.from_string(string_to_print, f'./{project_id}.pdf')
    return redirect(url_for('projects_list'))


# Proyectos de un usuario
@app.route('/projects/user_projects')
def user_projects():
    """Renderiza la vista con la lista de proyectos de un usuario.
        El Id del usuario se obtiene por url args"""
    
    users_projects_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'Description', 'class': 'col-6'},
        {'label': 'Start', 'class': 'col-2'},
        {'label': 'End', 'class': 'col-2'}        
    ]

    user_id = request.args['id']
    user = db.session.query(User).filter_by(id=user_id).first()
    projects = db.session.query(Project).all()
    projects_user_is = []
    for p in projects :
        for u in p.users:
            if (u.id == user.id):
                projects_user_is.append({
                    'data' : [p.id, p.description, p.start.strftime(f'%m-%d-%Y'), p.finish.strftime(f'%m-%d-%Y')]
                })

    return render_template('projects/user_projects.html',
        username=user,   
        list_context= {
                'list_header': users_projects_list_header,
                'list_body' : projects_user_is
            })
