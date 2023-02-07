from flask import Flask
from src.config import DevConfig
from src.models import db

app = Flask(__name__, template_folder='src/templates')
app.config.from_object(DevConfig)

from src.routes import routes

db.init_app(app)
if __name__== '__main__':
    app.run()
