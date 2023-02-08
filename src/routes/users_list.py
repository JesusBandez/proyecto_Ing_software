from flask import render_template
from . import app

@app.route('/users_list')
def users_lists():
    return render_template(
        'users_list/users_list.html'       
    )