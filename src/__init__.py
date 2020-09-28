from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import os

# _____ INIT + CONFIG ______
#Create a flask app
sys.path.append('.')
sys.path.append('../src')
app = Flask(__name__)

#app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# create database tables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
# print("triggered")

from src import models
db.create_all()

# _____ TEMP ______
from src.models import Concept
# from src.models import User

@app.route('/')
def hello():
    print("triggered")
    return "Hello World!"

@app.route('/concept_test')
def concept_test():
    cs = Concept.query.all()
    ctitle = [c.title for c in cs]
    return str(ctitle)

# _____ MAIN ______

if __name__ == '__main__':
    # app.run(ssl_context=('cert.pem', 'key.pem'), threaded=True, port=5001)
    app.run()
