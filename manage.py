from main import app, db
from src.models.User import User



@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User,
        create_admin=create_admin)


def create_admin():
    user = User('fadmin', 'ladmin', '1', '1', 'admin', 'Enginer')
    db.session.add(user)
    db.session.commit()