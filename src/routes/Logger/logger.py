from flask import render_template, request, session, redirect, url_for, flash
from src.models import db

from . import app


@app.route('/event_logger', methods=('GET', 'POST'))
def logger():   
    return render_template('logger/logger.html')