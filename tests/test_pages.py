import io
import json
import unittest
from tests.base import FlaskTestCase

class TestPageCase(FlaskTestCase):
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        self.app.post('login', data = dict(email="example@gmail.com", username="example", password="111"), follow_redirects=True)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_redirect(self):
        response = self.app.get('/artifacts/new', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        assert "Login to contribute" in str(response.data)

    def test_create_loggedin(self):
        self.app.post('login', data = dict(email="example@gmail.com", username="example", password="111"), follow_redirects=True)
        response = self.app.get('/artifacts/new', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        assert "id=\"artifact-form\"" in str(response.data)

if __name__ == '__main__':
    unittest.main()
