from flask import render_template, request, session, redirect, url_for, flash
from src.lib.generate_action import generate_action
from src.lib.class_create_button import ListEvents

from src.models import db
from src.models.Logger import Logger

from . import app
from sqlalchemy import extract  




def search_events(typeS,search):
    if typeS == "event":
        events = db.session.query(Logger).filter(Logger.event.contains(search))
    elif typeS == "month":
        events = db.session.query(Logger).filter(extract('month', Logger.date)==int(search))
    elif typeS == "day":
        events = db.session.query(Logger).filter(extract('day', Logger.date)==int(search))
    elif typeS == "year":
        events = db.session.query(Logger).filter(extract('year', Logger.date)==int(search))
    else:
        events = db.session.query(Logger).all()
    return events

@app.route('/event_logger', methods=('GET', 'POST'))
def logger():
    try:
        typeS = request.form['typeSearch']
        search = request.form['search']
        EVENTS = search_events(typeS,search)
        if EVENTS.count() == 0:
            EVENTS = db.session.query(Logger).all()
    except:
        EVENTS = db.session.query(Logger).all()

    A = ListEvents(EVENTS)
    events_list_body = A.list_table()
    users_list_header = A.header

    return render_template('logger/logger.html',
        list_context= {
            'list_header': users_list_header,
            'list_body' : events_list_body
        })

def removing_event(event_id):
    event = db.session.query(Logger).filter_by(id=event_id).first()

    db.session.delete(event)
    db.session.commit()
    return event


@app.route('/event_logger/remove_event', methods=('GET', 'POST'))
def remove_event():
    event_id = request.form['id']
    e = removing_event(event_id)
    
    return redirect(url_for('logger'))

@app.route('/event_logger/foo_event', methods=('GET', 'POST'))
def foo_event():
    # TODO: No tengo idea de que debe hacer esto
    print('Foo evento')
    return redirect(url_for('logger'))