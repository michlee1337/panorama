import io
import json
import unittest
from tests.base import FlaskTestCase

class TestPageCase(FlaskTestCase):
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_page(self):
        response = self.app.get('/artifacts/new', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
