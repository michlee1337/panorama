from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_login import LoginManager
import sys
import os

# Get Font Awesome
from flask_fontawesome import FontAwesome

# Create a flask app
sys.path.append('.')
sys.path.append('../src')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bonka'
login = LoginManager(app)
login.login_view = 'login.login'

# Plugins
bootstrap = Bootstrap(app)
fa = FontAwesome(app)

# app.static_folder = 'static'

# create database tables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

from src import models
db.create_all()

from src.models import User
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# register routes
# from blueprints.concepts import concepts_template
from blueprints.users import users_template
from blueprints.studyplans import studyplans_template
from blueprints.pages import pages_template

# app.register_blueprint(concepts_template)
app.register_blueprint(users_template)
app.register_blueprint(studyplans_template)
app.register_blueprint(pages_template)

# _____ MAIN ______

if __name__ == '__main__':
    app.run()
