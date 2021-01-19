import os
import io
import sys
import json
import glob
import unittest

os.environ["DATABASE_URL"] = "sqlite:///test.db"
from src import app, db, models

class FlaskTestCase(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        db.create_all()
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
