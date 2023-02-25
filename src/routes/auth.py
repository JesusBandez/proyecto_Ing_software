from flask import session
def has_role(role='user'):
    if not session.get('user'):
        return False

    if role == 'user':
        return session.get('user')['role'] == 'user' or session.get('user')['role'] == 'admin'
    elif role == 'admin':
        return session.get('user')['role'] == 'admin'

    raise Exception(f'Rol: {role} no reconocido')