import os
import io
import sys
import json
import glob
import unittest

os.environ["DATABASE_URL"] = "sqlite:///test.db"
from src import app
from src.models import db
from src.models.users import User

class FlaskTestCase(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        db.init_app(app)
        with app.app_context():
            db.create_all()

            example_user = User(
                id=1, email="example@gmail.com", username="example")
            example_user.set_password("111")
            db.session.merge(example_user)

            db.session.commit()

        self.app = app.test_client()

    def login(self):
        return self.app.post('login', data = dict(email="example@gmail.com", username="example", password="111"), follow_redirects=True)

    # executed after each test
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
