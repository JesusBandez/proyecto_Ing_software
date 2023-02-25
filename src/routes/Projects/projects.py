from flask import render_template, request, session, redirect, url_for, flash, send_from_directory
from src.lib.generate_action import generate_action
from src.routes.auth import has_role
from src.routes.Projects import project_details
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
    # TODO: No se que hace esta vaina pero la voy a usar para los detalles
    print("Generando")
    return redirect(url_for('project_details', id=request.args['id']))

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

@app.route('/projects/print_project', methods=['POST'])
def print_project():  
    "Muestra el formulario para agregar o editar un proyecto"
    project_id = request.form['id']
    project = db.session.query(Project).filter_by(id=project_id).first()
    show_project = {
        'id' : project.id,
        'description' : project.description,
        'start' : project.start.date(),
        'finish' : project.finish.date(),
        'users' : project.users
    }
    return render_template('print_project/print_project.html', 
        project=show_project)

@app.route('/projects/print_project', methods=['GET', 'POST'])
def generate_pdf():
    "Imprimir proyecto"
    project_id = request.args['id']
    project = db.session.query(Project).filter_by(id=project_id).first()
    show_project = {
        'id' : project.id,
        'description' : project.description,
        'start' : project.start.date(),
        'finish' : project.finish.date(),
        'users' : project.users
    }
    rendered = render_template('print_project/print_project.html', project=show_project)
    pdfkit.from_string(rendered, f'./printed/{project_id}.pdf')
    """ file_to_print = f'./printed/{project_id}.pdf'
    send_from_directory('./', file_to_print) """
    return redirect(url_for('projects_list'))

