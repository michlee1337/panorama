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

# TEST
# concept1 = models.Concept(
#     title = "Concept 1")
#
# concept2 = models.Concept(
#     title = "Concept 2")
#
# concept1.children.append(concept2)
#
# resource1 = models.Resource(name="google", link = "www.google.com", depth=0)
# resource2 = models.Resource(name="purple", link = "www.purple.com", depth=1)
# resource3 = models.Resource(name="github", link = "www.github.com", depth=2)
# concept1.resources.append(resource1)
# concept1.resources.append(resource2)
# concept2.resources.append(resource3)
# db.session.merge(resource1)
# db.session.merge(resource2)
# db.session.merge(resource3)
# db.session.merge(concept1)
# db.session.merge(concept2)
#
# db.session.commit()

# END TEST



# register routes
from blueprints.concepts import concepts_template
from blueprints.users import users_template

app.register_blueprint(concepts_template)
app.register_blueprint(users_template)

# _____ TEMP ______
@app.route('/')
def hello():
    return "Hello World! View <a href='concepts/1'>demo page </a>"

@app.route('/concept_test')
def concept_test():

    cs = Concept.query.all()
    print([str(c) for c in cs])
    ctitle = [c.title for c in cs]
    return str(ctitle)

@app.route('/resource_test')
def resource_test():

    cs = Resource.query.all()
    print([str(c) for c in cs])
    ctitle = [c.name for c in cs]
    return str(ctitle)

# _____ END TEMP ______

# _____ MAIN ______

if __name__ == '__main__':
    app.run()
