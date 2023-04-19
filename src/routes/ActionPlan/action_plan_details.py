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
    print(plan.human_talents)
    list_talents = ListHumanTalents(plan.human_talents, project_id)
    return render_template('action_plans/action_plan_detail.html',
        has_role=has_role,      
        context={ 'plan' : plan
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
    return redirect(url_for('action_plan_details'))


@app.route('/projects/action_plan_details/remove_human_talent')
def remove_human_talent():
    """ Elimina un human talent"""
    return redirect(url_for('action_plan_details'))
