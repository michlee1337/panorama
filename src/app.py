from flask import Flask
import sys

# _____ INIT + CONFIG ______
#Create a flask app
sys.path.append('src')
app = Flask(__name__)
#app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# setup and create database
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create database tables
# db.init_app(app)
# with app.app_context():
#     db.create_all()
#     db.session.commit()

# _____ TEMP ______

@app.route('/')
def hello():
    return "Hello World! src"


# _____ MAIN ______

if __name__ == '__main__':
    app.run()
