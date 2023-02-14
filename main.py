from flask import Flask
from src.config import DevConfig
from src.models import db

app = Flask(__name__, template_folder='src/templates')
app.config.from_object(DevConfig)

from src.routes.login import login
from src.routes.users_list import users_list
db.init_app(app)
if __name__== '__main__':
    app.run(host="0.0.0.0", port=7070)
