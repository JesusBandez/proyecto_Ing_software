from flask import render_template, request, session, redirect, url_for, flash

from src.lib.generate_action import generate_action
from src.lib.class_create_button import ListHumanTalents

from src.routes.auth import has_role, is_project_manager, require_permissions
from src.models import db
from src.models.Project import Project
from src.models.User import User
from src.models.Logger import Logger
from src.models.ActionPlan import ActionPlan
from src.models.HumanTalent import HumanTalent
from datetime import datetime

from src.errors import Errors, ERROR_MUST_BE_ADMIN, ERROR_MUST_BE_ADMIN_AND_MANAGER
from . import app

@app.route('/projects/action_plan_details')
def action_plan_details():
    """Renderiza los detalles de un plan de accion"""
    project_id = request.args['project_id']
    plan_id = request.args['id']
    plan = db.session.query(ActionPlan).filter_by(
        id=plan_id
    ).first()

    list_talents = ListHumanTalents(plan.human_talents, project_id, plan_id)
    return render_template('action_plans/action_plan_detail.html',
        has_role=has_role,      
        context={ 'plan' : plan,
            'project_id' : project_id,
            },   
        talents_list_context= {
            'list_header': list_talents.header,
            'list_body' : list_talents.list_table()
            },
        supplies_plans_list_context = {
             
        }
            )

@app.route('/projects/action_plan_details/new_human_talent')
def new_human_talent():
    """ Muestra el formulario para un nuevo talento"""
    talent_to_edit = request.args.get('id')
    project_id = request.args.get('project_id')
    action_plan_id = request.args.get('plan_id')

    talent = None
    if talent_to_edit:
        talent = db.session.query(HumanTalent).filter_by(id=talent_to_edit).first()
        title = 'Edit Human Talent'
    else:
        title = 'Add Human Talent'

    return render_template('action_plans/new_human_talent.html', 
        context={
            'talent': talent,
            'project_id' : project_id,
            'title' : title,
            'action_plan_id' : action_plan_id,
        })

@app.route('/projects/action_plan_details/add_new_human_talent', methods=['POST'])
def add_new_human_talent():
    """ Agrega al talento al sistema"""    
    project_id = request.form.get('project_id')
    action_plan_id = request.form.get('action_plan_id')

    action = request.form['action']
    activity = request.form['activity']
    time = request.form['time']
    quantity = request.form['quantity']
    responsible = request.form['responsible']
    cost = request.form['cost']

    talent_to_edit = request.form.get('talent_to_edit')    


    if not talent_to_edit:
        human_talent = HumanTalent(action, activity, time, 
            quantity, cost, responsible, action_plan_id)
        log = Logger('Adding human talent')
        db.session.add(log)
        db.session.add(human_talent)

    else:
        changes = {
            'action': action,
            'activity': activity,
            'time': time,
            'quantity': quantity,
            'responsible': responsible,
            'cost': cost,
        }
        db.session.query(HumanTalent).filter_by(
            id=talent_to_edit).update(changes)
        log = Logger('Editing Human talent')
        db.session.add(log)


    db.session.commit()    

    return redirect(url_for('action_plan_details', project_id=project_id, id=action_plan_id)
        + '#humantalent')


@app.route('/projects/action_plan_details/remove_human_talent', methods=['POST'])
def remove_human_talent():
    """ Elimina un human talent"""
    project_id = request.form.get('project_id')
    plan_id = request.form.get('plan_id')

    human_talent = db.session.query(HumanTalent).filter_by(id=request.form.get('id')).first()

    log = Logger('Deleting action plan')

    db.session.add(log)
    db.session.delete(human_talent)
    db.session.commit()

    return redirect(url_for('action_plan_details', project_id=project_id, id=plan_id)
        + '#humantalent')
