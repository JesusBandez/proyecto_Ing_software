from flask import session
def has_role(role='user'):
    return session.get('user') and session['user']['role'] == role