from flask import render_template, request, session, redirect, url_for, flash
from src.routes.auth import has_role
from src.models import db
from . import app


@app.route('/projects/list', methods=('GET', 'POST'))
def projects_list():
    "Renderiza la lista con todos los proyectos del sistema"

    users_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'Description', 'class': 'col-3'},
        {'label': 'Start', 'class': 'col-2'},
        {'label': 'End', 'class': 'col-2'},
        {'label': 'Actions', 'class': 'col-3'},        
    ]
    return render_template('projects/projects.html',
        has_role=has_role,
        list_context= {
                'list_header': users_list_header,
                'list_body' : [], # Meterle los datos
            })


@app.route('/projects/user_projects')
def user_projects():
    """Renderiza la vista con la lista de proyectos de un usuario.
        El Id del usuario se obtiener por url args"""

    print(request.args.get("id"))
    users_projects_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'Description', 'class': 'col-6'},
        {'label': 'Start', 'class': 'col-2'},
        {'label': 'End', 'class': 'col-2'}        
    ]
    return render_template('projects/user_projects.html',        
        list_context= {
                'list_header': users_projects_list_header,
                'list_body' : [], # Meterle los datos
            })

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