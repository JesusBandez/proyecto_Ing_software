from flask import render_template, request, session, redirect, url_for, flash,jsonify

from src.lib.generate_action import generate_action
from src.lib.class_create_button import ListHumanTalents, ListMaterialSupplies

from src.routes.auth import has_role, is_project_manager, require_permissions
from src.models import db
from src.models.Project import Project
from src.models.User import User
from src.models.Logger import Logger
from src.models.ActionPlan import ActionPlan
from src.models.HumanTalent import HumanTalent
from src.models.MaterialsSupplies import MaterialsSupplies
from datetime import datetime

from src.errors import Errors, ERROR_MUST_BE_ADMIN, ERROR_MUST_BE_ADMIN_AND_MANAGER
from . import app


@app.route("/ajaxlivesearchresp",methods=["POST","GET"])
def ajaxlivesearchresp():
    if request.method == 'POST':
        search_word = request.form['search']

        if search_word != '':
            users = db.session.query(User).filter((User.first_name + User.last_name).contains(search_word)).all()
        else:
            users = db.session.query(User).all()
        all_info = []
        for user in users:
            all_info.append(user)
    return jsonify({'htmlresponse': render_template('action_plans/table_for_responsible.html', all_info=all_info)})
     


def searchTalents(typeS,search,plan_id):
    if typeS == "activity":
        talents = db.session.query(HumanTalent).filter(HumanTalent.plan == plan_id, HumanTalent.activity.contains(search))
    elif typeS == "action":
        talents = db.session.query(HumanTalent).filter(HumanTalent.plan == plan_id, HumanTalent.action.contains(search))
    elif typeS == "responsible":
        talents = db.session.query(HumanTalent).filter(HumanTalent.plan == plan_id, HumanTalent.responsible.contains(search))
    return talents


@app.route('/projects/action_plan_details', methods=('GET', 'POST'))
def action_plan_details():
    """Renderiza los detalles de un plan de accion"""
    project_id = request.args['project_id']
    plan_id = request.args['id']
    plan = db.session.query(ActionPlan).filter_by(
        id=plan_id
    ).first()

    try:
        typeS = request.form['typeSearch']
        search = request.form['search']
        talents = searchTalents(typeS,search,int(plan_id))
        if talents.count() == 0:
            talents = plan.human_talents
    except:
        talents = plan.human_talents

    list_talents = ListHumanTalents(talents, project_id, plan_id)    

    # TODO: Implementar la busqueda de supplies
    supplies = plan.supplies
    list_supplies = ListMaterialSupplies(supplies, project_id, plan_id)


    return render_template('action_plans/action_plan_detail.html',
        has_role=has_role,      
        context={ 'plan' : plan,
            'project_id' : project_id,
            'total_talent_cost' : plan.human_talent_costs(),
            'total_supplies_cost' : plan.supplies_costs(),
            'total_project_cost' : plan.plan_cost()
            },   
        talents_list_context= {
            'list_header': list_talents.header,
            'list_body' : list_talents.list_table()
            },
        supplies_plans_list_context = {
            'list_header': list_supplies.header,
            'list_body' : list_supplies.list_table()             
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
    responsible = request.form['responsible_selection']
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



@app.route('/projects/action_plan_details/new_supply')
def new_supply():
    """ Muestra el formulario para un nuevo material"""
    supply_to_edit = request.args.get('id')
    project_id = request.args.get('project_id')
    action_plan_id = request.args.get('plan_id')

    supply = None
    if supply_to_edit:
        supply = db.session.query(MaterialsSupplies).filter_by(id=supply_to_edit).first()
        title = 'Edit Suply'
    else:
        title = 'Add Suply'

    return render_template('action_plans/new_supply.html', 
        context={
            'supply': supply,
            'project_id' : project_id,
            'title' : title,
            'action_plan_id' : action_plan_id,
        })

@app.route('/projects/action_plan_details/add_new_supply', methods=['POST'])
def add_new_supply():
    """ Agrega el material al sistema"""    
    project_id = request.form.get('project_id')
    action_plan_id = request.form.get('action_plan_id')

    action = request.form['action']
    activity = request.form['activity']
    category = request.form['category']
    description = request.form['description']
    quantity = request.form['quantity']
    measure = request.form['measure']
    cost = request.form['cost']
    responsible = request.form['responsible']

    supply_to_edit = request.form.get('supply_to_edit')    


    if not supply_to_edit:
        human_talent = MaterialsSupplies(action, activity, category, description,
            quantity, measure, cost, responsible, action_plan_id)
        log = Logger('Adding supply')
        db.session.add(log)
        db.session.add(human_talent)

    else:
        changes = {
            'action': action,
            'activity': activity,
            'category': category,
            'description' : description,
            'quantity': quantity,
            'measure' : measure,
            'cost': cost,
            'responsible': responsible,
        }
        db.session.query(MaterialsSupplies).filter_by(
            id=supply_to_edit).update(changes)
        log = Logger('Editing Human talent')
        db.session.add(log)


    db.session.commit()    

    return redirect(url_for('action_plan_details', project_id=project_id, id=action_plan_id)
        + '#supplies')

@app.route('/projects/action_plan_details/remove_supply', methods=['POST'])
def remove_supply():
    """ Elimina un supply"""
    project_id = request.form.get('project_id')
    plan_id = request.form.get('plan_id')

    supply = db.session.query(MaterialsSupplies).filter_by(id=request.form.get('id')).first()

    log = Logger('Deleting action plan')

    db.session.add(log)
    db.session.delete(supply)
    db.session.commit()

    return redirect(url_for('action_plan_details', project_id=project_id, id=plan_id)
        + '#supplies')