from flask import render_template, request, session, redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.models import db
from src.models.Logger import Logger

from . import app


@app.route('/event_logger', methods=('GET', 'POST'))
def logger():
    users_list_header = [
        {'label': 'Id', 'class': 'col-1'},
        {'label': 'Event', 'class': 'col-3'},
        # {'label': 'Module', 'class': 'col-1'},
        {'label': 'Date', 'class': 'col-2'},
        {'label': 'Hour', 'class': 'col-1'},
        {'label': 'Actions', 'class': 'col-2'},
    ]

    EVENTS = db.session.query(Logger).all()
    events_list_body = []
    for event in EVENTS:
        remove = generate_action(event.id, 'remove_event', 'post',
            button_class='btn btn-sm btn-danger w-100',
            title="Remove event",
            text_class='fa-solid fa-trash')

        foo = generate_action(event.id,
            'foo_event', button_class='btn btn-sm btn-info w-100',
            title="Foo event",
            text_class='fa-solid fa-table-list')
        
        events_list_body.append({
            'data' : [event.id, event.event, 
                    event.date.strftime(f'%m-%d-%Y'), event.hour.strftime(f'%H:%M:%S')],
            'actions' : [remove, foo]
            })

    return render_template('logger/logger.html',
        list_context= {
            'list_header': users_list_header,
            'list_body' : events_list_body
        })

@app.route('/event_logger/remove_event', methods=('GET', 'POST'))
def remove_event():
    event_id = request.form['id']
    event = db.session.query(Logger).filter_by(id=event_id).first()

    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('logger'))

@app.route('/event_logger/foo_event', methods=('GET', 'POST'))
def foo_event():
    # TODO: No tengo idea de que debe hacer esto
    print('Foo evento')
    return redirect(url_for('logger'))