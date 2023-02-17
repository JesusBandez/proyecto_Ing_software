from flask import render_template, request, session, redirect, url_for, flash
from src.models import db

from . import app


@app.route('/event_logger', methods=('GET', 'POST'))
def logger():
    users_list_header = [
        {'label': 'Id', 'style': 'width: 5%'},
        {'label': 'Event', 'style': 'width: 20%'},
        {'label': 'Module', 'style': 'width: 20%'},
        {'label': 'Date', 'style': 'width: 20%'},
        {'label': 'Hour', 'style': 'width: 15%'},
        {'label': 'Actions', 'style': 'width: 15%'},
    ]
    return render_template('logger/logger.html',
        list_context= {
            'list_header': users_list_header,
            'list_body' : [], # Meterle los datos
        })