from flask import render_template, request, session, redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.lib.class_create_button import ListProjectsUser, ListManageProjectUsers, ListActionPlansList

from src.routes.auth import has_role, is_project_manager, require_permissions
from src.models import db
from src.models.Project import Project
from src.models.User import User
from src.models.Logger import Logger
from src.models.ActionPlan import ActionPlan
from datetime import datetime

from src.errors import Errors, ERROR_MUST_BE_ADMIN, ERROR_MUST_BE_ADMIN_AND_MANAGER
from . import app

@app.route('/projects/action_plan_details')
def action_plan_details():
    """Renderiza los detalles de un plan de accion"""

    plan = db.session.query(ActionPlan).first()


    return render_template('action_plans/action_plan_detail.html',
        has_role=has_role,      
        context={ 'plan' : plan
            },   
        users_list_context= {
                
            },
        actions_plans_list_context = {
             
        }
            )

