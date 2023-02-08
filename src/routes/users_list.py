from flask import render_template, redirect, url_for, request
from src.models.User import User
from . import app

@app.route('/users_list')
def users_lists():
    return render_template(
        'users_list/users_list.html'
        , users=[User("Coronao"), User("Chang"), User("Yriarte"), User("EB"), User("Fernando")] # Aqui va la lista de usuarios de la base de datos. Deberiamos agregar paginacion???   
    )

@app.route('/users_list/delete', methods=['GET', 'POST'])
def delete_user():
    user_id = request.form['id']
    # Eliminar al usuario de la base
    # TODO
    return redirect(url_for('users_lists'))