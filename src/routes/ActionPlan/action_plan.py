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


def deleting(action_plan_id):
    action_plan = db.session.query(ActionPlan).filter_by(id=action_plan_id).first()

    log = Logger('Deleting action plan')

    db.session.add(log)
    for element in action_plan.supplies:        
        db.session.delete(element)
    for element in action_plan.human_talents:        
        db.session.delete(element)

    db.session.delete(action_plan)
    db.session.commit()
    return [log,action_plan]

@app.route('/action_plans_list/delete', methods=['GET', 'POST'])
@require_permissions
def delete_action_plan():
    "Elimina un plan de accion del sistema"
        
    action_plan_id = request.form['id']
    deleting(action_plan_id)
    project_id = request.form['project_id']
    
    return redirect(f"{url_for('project_details', id=project_id)}#actionplan")


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


def create_action_plan(action, activity, start_date, close_date, quantity, responsible, project):

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

    if error:
        return [error,False]

    if error is None:
        action_plan = ActionPlan(action, activity, start_date, close_date, 
            quantity, responsible, project)

        log = Logger('Adding action plan')

        db.session.add(log)
        db.session.add(action_plan)
        db.session.commit()
        return [action_plan,True]


@app.route('/action_plans_list/add_new_action_plan', methods=['POST'])
def add_new_action_plan():
    "Agrega un nuevo plan de accion al sistema"

    action = request.form['action']
    activity = request.form['activity']
    start_date = datetime.strptime(request.form['s_date'], r'%Y-%m-%d')
    close_date = datetime.strptime(request.form['c_date'], r'%Y-%m-%d')
    quantity = request.form['quantity']
    responsible = request.form['responsible_selection']   

    action_plan_to_edit = request.form.get('action_plan_to_edit')


    if not action_plan_to_edit:
        project = request.form['project_id']
        action_plan = create_action_plan(action, activity, start_date, close_date, 
                quantity, responsible, project)

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