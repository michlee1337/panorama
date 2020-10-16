from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# Get Font Awesome
from flask_fontawesome import FontAwesome
import sys
import os

# Create a flask app
sys.path.append('.')
sys.path.append('../src')
app = Flask(__name__)

# Get Font Awesome
fa = FontAwesome(app)

# app.static_folder = 'static'

# create database tables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

from src import models
db.create_all()

# TEST
# concept1 = models.Concept(
#     title = "Concept 1")
#
# concept2 = models.Concept(
#     title = "Concept 2")
#
# concept1.children.append(concept2)
#
# db.session.merge(concept1)
# db.session.merge(concept2)
#
# db.session.commit()

# END TEST



# register routes
from blueprints.concepts import concepts_template

app.register_blueprint(concepts_template)

# _____ TEMP ______
@app.route('/')
def hello():
    return "Hello World!"

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
