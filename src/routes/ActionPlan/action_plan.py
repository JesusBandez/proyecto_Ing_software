from flask import render_template, redirect, url_for, request, flash, session
from datetime import datetime
from src.routes.auth import has_role, require_permissions, error_display

from src.lib.class_create_button import ListActionPlansList

from src.models.ActionPlan import ActionPlan
from src.models.Project import Project
from src.models.Logger import Logger
from src.models import db
from src.lib.generate_action import generate_action
from src.errors import Errors, ERROR_ACTION_PLAN_ALREADY_EXISTS

from . import app

def search_action_plans(typeS,search):
    if typeS == "action":
        action_plans = db.session.query(ActionPlan).filter(ActionPlan.action.contains(search))
    elif typeS == "activity":
        action_plans = db.session.query(ActionPlan).filter(ActionPlan.activity.contains(search))
    else:
        action_plans = db.session.query(ActionPlan).all()
    return action_plans

@app.route('/action_plans_list', methods=['GET', 'POST'])
def action_plans_lists():
    #"Muestra la lista de medidas del sistema"
    try:
        typeS = request.form['typeSearch']
        search = request.form['search']
        action_plans = search_action_plans(typeS,search)
        if action_plans.count() == 0:
            action_plans = db.session.query(ActionPlan).all()
    except:
        action_plans = db.session.query(ActionPlan).all()

    A = ListActionPlansList(action_plans)
    action_plans_list_body = A.list_table()
    action_plans_list_header = A.header

    return render_template(
        'action_plans/action_plans_list.html',
        has_role=has_role,
        list_context= {
            'list_header': action_plans_list_header,
            'list_body' : action_plans_list_body,
        })

def deleting(action_plan_id):
    action_plan = db.session.query(ActionPlan).filter_by(id=action_plan_id).first()

    log = Logger('Deleting action plan')

    db.session.add(log)
    db.session.delete(action_plan)
    db.session.commit()
    return [log,action_plan]

@app.route('/action_plans_list/delete', methods=['GET', 'POST'])
@require_permissions
def delete_action_plan():
    "Elimina un plan de accion del sistema"
        
    action_plan_id = request.form['id']
    z = deleting(action_plan_id)
    
    return redirect(url_for('action_plans_lists'))


@app.route('/action_plans_list/new_action_plan', methods=['POST', 'GET'])
@require_permissions
def new_action_plan():
    "Renderiza el formulario de registro de un nuevo plan de accion"
    
    action_plan_to_edit = db.session.query(ActionPlan).filter_by(
            id=request.form.get('id')).first()

    project_id = request.args.get('project_id')
    if action_plan_to_edit: 
        project_id = action_plan_to_edit.project

    c_date = None
    s_date = None
    if not action_plan_to_edit:
        title = 'Register New Action Plan'
    else:
        title = 'Edit Action Plan'
        c_date = action_plan_to_edit.finish_date.date()
        s_date = action_plan_to_edit.start_date.date()

    print(project_id)
    return render_template('action_plans/new_action_plan.html', 
        context={
            'action_plan_to_edit': action_plan_to_edit,
            'title': title,
            'project_id' : project_id,
            'c_date':c_date,
            's_date' : s_date
        })


def create_action_plan(action, activity, start_date, close_date, quantity, responsible, cost, project):

    error = None
    if not action:
        error = 'Action is required.'
    elif not activity:
        error = 'Activity is required.'
    elif not start_date:
        error = 'Start date is required.'
    elif not close_date:
        error = 'Close date is required.'
    elif not quantity:
        error = 'Quantity is required.'
    elif not responsible:
        error = 'Responsible is required.'
    elif not cost:
        error = 'Cost is required.'

    action_plan = db.session.query(ActionPlan).filter_by(activity=activity).first()
    if action_plan:
        error = f'Activity {activity} is already created.'

    if error:
        return [error,False]

    if error is None:
        action_plan = ActionPlan(action, activity, start_date, close_date, 
            quantity, responsible, cost, project)

        log = Logger('Adding action plan')

        db.session.add(log)
        db.session.add(action_plan)
        db.session.commit()
        return [action_plan,True]


def verify_action_plan_exist(guser_id, activity):
    if guser_id is not None:
        action_plan_id = int(guser_id)
    else:
        return False
    action_plan = db.session.query(ActionPlan).filter_by(id=action_plan_id).first()
    if action_plan != None and activity != action_plan.activity:
        return True
    return False


@app.route('/action_plans_list/add_new_action_plan', methods=['POST'])
def add_new_action_plan():
    "Agrega un nuevo plan de accion al sistema"

    action = request.form['action']
    activity = request.form['activity']
    start_date = datetime.strptime(request.form['s_date'], r'%Y-%m-%d')
    close_date = datetime.strptime(request.form['c_date'], r'%Y-%m-%d')
    quantity = request.form['quantity']
    responsible = request.form['responsible']
    cost = request.form['cost']    

    action_plan_to_edit = request.form.get('action_plan_to_edit')

    already_exists = verify_action_plan_exist(action_plan_to_edit, activity)

    if already_exists:
        error_display(ERROR_ACTION_PLAN_ALREADY_EXISTS)
        return redirect(url_for('action_plans_lists'))

    if not action_plan_to_edit:
        project = request.form['project_id']
        action_plan = create_action_plan(action, activity, start_date, close_date, 
                quantity, responsible, cost, project)

        if action_plan[1] == False:
            error_display(ERROR_ACTION_PLAN_ALREADY_EXISTS)
            return redirect(url_for('new_action_plan', project_id=project))
    else:
        changes = {
            'action': action,
            'activity': activity,
            'start_date': start_date,
            'finish_date': close_date,
            'hours': quantity,
            'responsible': responsible,
            'cost': cost,
        }
        action_plan = db.session.query(ActionPlan).filter_by(
            id=action_plan_to_edit).update(changes)
        log = Logger('Editing action plan')
        db.session.add(log)
        action_plan = db.session.query(ActionPlan).filter_by(
            id=action_plan_to_edit).first()
        project = action_plan.project

    db.session.commit()

    return redirect(f"{url_for('project_details', id=project)}#actionplan")