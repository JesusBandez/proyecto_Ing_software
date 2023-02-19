from flask import render_template, request, session, redirect, url_for, flash
from src.models import db

from . import app


@app.route('/event_logger', methods=('GET', 'POST'))
def logger():
    users_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'Event', 'class': 'col-3'},
        {'label': 'Module', 'class': 'col-1'},
        {'label': 'Date', 'class': 'col-2'},
        {'label': 'Hour', 'class': 'col-1'},
        {'label': 'Actions', 'class': 'col-2'},
    ]
    return render_template('logger/logger.html',
        list_context= {
            'list_header': users_list_header,
            'list_body' : [], # Meterle los datos
        })