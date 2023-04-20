from flask import render_template, redirect, url_for, request, flash, session
from src.routes.auth import has_role, require_permissions, error_display
from manage import init_db
from src.lib.class_create_button import ListMeasuresList

from src.models.Measures import Measures
from src.models.Logger import Logger
from src.models import db
from src.lib.generate_action import generate_action
from src.errors import Errors, ERROR_MEASURE_ALREADY_EXISTS

from . import app

def search_measures(typeS,search):
    if typeS == "dimension":
        measures = db.session.query(Measures).filter(Measures.dimension.ilike(f'%{search}%'))
    elif typeS == "unit":
        measures = db.session.query(Measures).filter(Measures.unit.ilike(f'%{search}%'))
    else:
        measures = db.session.query(Measures).all()
    return measures

@app.route('/measures_list', methods=['GET', 'POST'])
def measures_lists():
    #"Muestra la lista de medidas del sistema"
    try:
        typeS = request.form['typeSearch']
        search = request.form['search']
        measures = search_measures(typeS,search)
        if measures.count() == 0:
            measures = db.session.query(Measures).all()
    except:
        measures = db.session.query(Measures).all()

    A = ListMeasuresList(measures)
    measures_list_body = A.list_table()
    measures_list_header = A.header

    return render_template(
        'measures/measures_list.html',
        has_role=has_role,
        list_context= {
            'list_header': measures_list_header,
            'list_body' : measures_list_body,
        })

def deleting(measure_id):
    measure = db.session.query(Measures).filter_by(id=measure_id).first()

    log = Logger('Deleting measure')

    db.session.add(log)
    db.session.delete(measure)
    db.session.commit()
    return [log,measure]

@app.route('/measure_list/delete', methods=['GET', 'POST'])
@require_permissions
def delete_measure():
    "Elimina una medida del sistema"
        
    measure_id = request.form['id']
    z = deleting(measure_id)
    
    return redirect(url_for('measures_lists'))


@app.route('/measures_list/new_measure', methods=['POST', 'GET'])
@require_permissions
def new_measure():
    "Renderiza el formulario de registro de una nueva medida"
    
    measure_to_edit = db.session.query(Measures).filter_by(
            id=request.form.get('id')).first()

    if not measure_to_edit:
        title = 'Register New Unit Of Measurement'
    else:
        title = 'Edit Unit Of Measurement'


    return render_template('measures/new_measure.html', 
        context={
            'measure_to_edit': measure_to_edit,
            'title': title,
        })


def create_measure(dimension, unit):
    error = None
    if not dimension:
        error = 'Dimension is required.'
    elif not unit:
        error = 'Unit is required.'

    measure = db.session.query(Measures).filter_by(dimension=dimension).first()
    if measure:
        error = f'Dimension {dimension} is already created.'

    if error:
        return [error,False]

    if error is None:
        measure = Measures(dimension, unit)

        log = Logger('Adding measure')

        db.session.add(log)
        db.session.add(measure)
        db.session.commit()
        return [measure,True]


def verify_measure_exist(guser_id, dimension, unit):
    if guser_id is not None:
        measure_id = int(guser_id)
    else:
        return False
    measure = db.session.query(Measures).filter_by(id=measure_id).first()

    if measure != None and dimension == measure.dimension and unit == measure.unit:
        return True
    return False


@app.route('/measures_list/add_new_measure', methods=['POST'])
def add_new_measure():
    "Agrega una nueva medida al sistema"

    dimension = request.form['dimension']
    unit = request.form['unit']

    measure_to_edit = request.form.get('measure_to_edit')

    already_exists = verify_measure_exist(measure_to_edit, dimension, unit)

    if already_exists:
        error_display(ERROR_MEASURE_ALREADY_EXISTS)
        return redirect(url_for('measures_lists'))

    if not measure_to_edit:
        measure = create_measure(dimension, unit)
        if measure[1] == False:
            error_display(ERROR_MEASURE_ALREADY_EXISTS)
            return redirect(url_for('new_measure'))
    else:
        changes = {
            'dimension' : dimension,
            'unit' : unit,
        }
        db.session.query(Measures).filter_by(
            id=measure_to_edit).update(changes)
        log = Logger('Editing measure')
        db.session.add(log)

    db.session.commit()

    return redirect(url_for('measures_lists'))




# TESTING
@app.route('/restart_bbdd')
def restart_bbdd():
    "Reinica la BBDD"

    db.drop_all()
    init_db()
    return ''
