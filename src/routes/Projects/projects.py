from flask import render_template, request, session, redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.routes.auth import has_role
from src.models import db
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
        {'label': 'Actions', 'class': 'col-4'},        
    ]

    # TODO: Obtener los proyectos del sistema.
    projects = [{'available': True, 'id': '1'}]
    projects_list_body = []
    for project in projects:
    
        generate = generate_action(project['id'],
            'generate_project', button_class='btn btn-sm btn-info w-100',
            text_class='fa-regular fa-rectangle-list',
            title="Generate project",
            disabled=not project['available'])

        edit = generate_action(project['id'],
            'edit_project', button_class='btn btn-sm btn-info w-100',
            title="Edit project",
            text_class='fa-solid fa-pencil',
            disabled=not project['available'])

        remove = generate_action(project['id'],
            'remove_project', button_class='btn btn-sm btn-danger w-100',
            title="Remove project",
            text_class='fa-solid fa-trash',
            disabled=not project['available'])

        toggle_availability = generate_action(project['id'],
            'toggle_project_availability',
            text_class= 'fa-solid fa-ban' if project['available'] else 'fa-solid fa-play',
            title="Disable project" if project['available'] else "Enable project",
            button_class='btn btn-sm btn-info w-100')

        print_project = generate_action(project['id'],            
            'print_project', 
            text_class='fa-solid fa-print',
            title="Print project",
            button_class='btn btn-sm btn-info w-100')         
     

    return render_template('projects/projects.html',
        has_role=has_role,
        list_context= {
                'list_header': users_list_header,
                'list_body' : [{'data': ['1', '1', '1', '1'],
                    'actions': [generate, edit, toggle_availability, 
                                print_project, remove]}], # Meterle los datos
            })

# Agregar proyectos
@app.route('/projects/new_project')
def new_project():  
    "Muestra el formulario para agregar nuevo proyecto"   
    return render_template('projects/new_project.html')

@app.route('/projects/new_project/add', methods=['POST'])
def add_new_project():
    """Obtiene los datos para agregar un nuevo proyecto y 
        lo agrega al sistema"""

    description = request.form['description']
    start_date = request.form['s_date']
    close_date = request.form['c_date']
    print(description)
    print(start_date)
    print(close_date)
        
    return redirect(url_for('projects_list'))


@app.route('/projects/list/generate_project', methods=['GET', 'POST'])
def generate_project():
    "Generar proyecto"
    print("Generando")
    return redirect(url_for('projects_list'))

@app.route('/projects/list/edit_project', methods=['GET', 'POST'])
def edit_project():
    "Editar proyecto"
    print("Editando")
    return redirect(url_for('projects_list'))

@app.route('/projects/list/remove_project', methods=['GET', 'POST'])
def remove_project():
    "Eliminar proyecto"
    print("Eliminando")
    return redirect(url_for('projects_list'))

@app.route('/projects/list/toggle_project_availability', methods=['GET', 'POST'])
def toggle_project_availability():
    "Habilitar/desabilitar proyecto"
    print("hab/dehab")
    return redirect(url_for('projects_list'))

@app.route('/projects/list/print_project', methods=['GET', 'POST'])
def print_project():
    "Imprimir proyecto"
    print("impr")
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

    
    #TODO: Se busca en la base de datos el usuario por su id. 
    # Mostrar error en caso de que no exista
    print(request.args.get("id"))
    user = {'username': 'dummy'}

    return render_template('projects/user_projects.html',
        username=user['username'],   
        list_context= {
                'list_header': users_projects_list_header,
                'list_body' : [], # Meterle los datos
            })
