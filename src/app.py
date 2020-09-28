from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import os

# _____ INIT + CONFIG ______
#Create a flask app
sys.path.append('src')
app = Flask(__name__)

#app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# create database tables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# _____ TEMP ______

@app.route('/')
def hello():
    return "Hello World!"


# _____ MAIN ______

if __name__ == '__main__':
    app.run()
