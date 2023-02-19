from main import app, db
from src.models.User import User



@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User,
        create_default_users=create_default_users)


def create_default_users():
    users = [User('fadmin', 'ladmin', '1', '1', 'admin', 'Enginer'),
            User('fadmin2', 'ladmin2', '2', '2', 'admin', 'Cleaner'),
            User('fadmin3', 'ladmin3', '3', '3', 'admin', 'Boss'),
            User('fuser', 'luser', '4', '4', 'admin', 'Enginer'),
            ]
    db.session.add_all(users)
    db.session.commit()