from flask import session
def has_role(role='user'):
    if not session.get('user'):
        return False

    if role == 'user':
        return session.get('user')['role'] == 'user' or session.get('user')['role'] == 'admin'
    elif role == 'admin':
        return session.get('user')['role'] == 'admin'

    raise Exception(f'Rol: {role} no reconocido')

def is_project_manager(project):
    '''Comprueba si el usuario logeado es el manager del proyecto. 
    Retorna False si el proyecto no tiene manager'''
    if not session.get('user'):
        return False

    return project.manager_id != None and session['user']['id'] == project.manager_id
    
