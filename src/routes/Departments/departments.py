from flask import render_template, request, redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.routes.auth import has_role
from src.models.Department import Department
from src.models.Logger import Logger
from src.models import db
from src.errors import Errors, ERROR_MUST_BE_ADMIN, ERROR_MUST_BE_ADMIN_ADD_CLIENT

from . import app


def search_departments(typeS, search):
    if not typeS or typeS == 'Search By':
        return db.session.query(Department).all()
    
    if typeS == 'description':
        DEPARTMENTS = db.session.query(Department)\
            .filter(Department.description.ilike(search)).all()
    
    if len(DEPARTMENTS) == 0:
        return db.session.query(Department).all()

    return DEPARTMENTS

# Departamentos del sistema
@app.route('/departments/list', methods=('GET', 'POST'))
def departments_list():
    "Renderiza la lista con todos los departamentos del sistema"

    departments_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'Description', 'class': 'col'},
        {'label': 'Actions', 'class': 'col-2'}, 
    ]

    DEPARTMENTS = search_departments(
        request.form.get('typeSearch'), 
        request.form.get('search'))

    departments_list_body = []
    for department in DEPARTMENTS:
        edit = generate_action(department.id, 'new_department', 'get', 
            button_class='btn btn-sm btn-outline-success',
            title="Edit department",
            text_class='fa-solid fa-pencil',
            disabled= not has_role('opera'))

        remove = generate_action(department.id, 'remove_department', 'post',
            button_class='btn btn-sm btn-outline-danger',
            title="Remove department",
            text_class='fa-solid fa-trash',
            disabled= not has_role('opera'))
        
        departments_list_body.append({
            'data' : [department.id, department.description],
            'actions' : [edit, remove]
            })
     
    return render_template('departments/departments.html',
        has_role=has_role,
        list_context= {
                'list_header': departments_list_header,
                'list_body' : departments_list_body
            })


@app.route('/departments/new_department')
def new_department():
    "Muestra el formulario para agregar o editar un departamento" 
    if not has_role('opera'):
        title = Errors(ERROR_MUST_BE_ADMIN_ADD_CLIENT).error.title
        desc = Errors(ERROR_MUST_BE_ADMIN_ADD_CLIENT).error.description
        flash(True, 'error')
        flash(title, 'error_title') 
        flash(desc, 'error_description')
        return redirect(url_for('departments_list'))

    department = db.session.query(Department).filter_by(id=request.args.get('id')).first()
    page_title = 'Edit department' if department else 'Add new department'
    
    return render_template('departments/new_department.html', context={
        'department' : department,
        'page_title' : page_title, 
    }) 


@app.route('/departments/new_department/add_department', methods=['POST'])
def add_new_department():
    """Obtiene los datos para agregar un nuevo departamento y 
        lo agrega al sistema"""

    department_to_edit = request.form.get('department_to_edit')

    if department_to_edit:
        changes = {
            'description' : request.form['description'],            
        }
        db.session.query(Department).filter_by(
            id=department_to_edit).update(changes)
        log = Logger('Editing department')
        db.session.add(log)

    else:
        department = Department(request.form['description'])
        log = Logger('Adding department')
        db.session.add_all([log, department]) 

    db.session.commit()
    return redirect(url_for('departments_list'))


@app.route('/departments/list/remove_project', methods=['GET', 'POST'])
def remove_department():
    """Elimina un departamento del sistema"""
    department = db.session.query(Department).filter_by(
        id=request.form['id']).first()
    log = Logger('Deleting department')
    db.session.add(log)
    db.session.delete(department)
    db.session.commit()
    return redirect(url_for('departments_list'))
