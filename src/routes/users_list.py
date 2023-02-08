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
    # Eliminar al usuario de la base de datos
    # TODO
    return redirect(url_for('users_lists'))

@app.route('/users_list/new_user')
def new_user():
    return render_template('users_list/new_user.html')

@app.route('/users_list/add_new_user', methods=['POST'])
def add_new_user():
    # Agregar el nuevo usuario a la base de datos
    # TODO
    print(request.form['username'])
    print(request.form['password'])
    print(request.form['permissions'])
    return redirect(url_for('users_lists'))