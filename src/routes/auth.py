from flask import session
def has_role(role='user'):
    '''Comprueba si un usuario tiene un determinado rol de permisos
    role : Rol que se comprueba que el usuario cumple
    El rol del usuario logeado se encuentra en session['user']['role'] 
    '''

    if not session.get('user'):
        return False

    if role == 'user':
        return session.get('user')['role'] in ['user', 'opera', 'admin']

    elif role == 'opera':
        return session.get('user')['role'] in ['opera', 'admin']

    elif role == 'admin':
        return session.get('user')['role'] == 'admin'

    raise Exception(f'Rol: {role} no reconocido')

def is_project_manager(project):
    '''Comprueba si el usuario logeado es el manager del proyecto. 
    Retorna False si el proyecto no tiene manager'''
    if not session.get('user'):
        return False

    return project.manager_id != None and session['user']['id'] == project.manager_id
    
