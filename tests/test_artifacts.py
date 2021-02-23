import io
import json
import unittest
from tests.base import FlaskTestCase
from src import app, db, models
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

class TestArtifactCase(FlaskTestCase):
    def __init__(self, *args, **kwargs):
        super(TestArtifactCase, self).__init__(*args, **kwargs)
        self.attrs = {"title":"1",
            "main_concept":"2",
            "mediatype":"0",
            "duration":"0",
            "prerequisites": "test",
            "chunks-0-concept": "test",
            "chunks-0-title": "test",
            "chunks-0-content": "test"}

    def test_create_simple(self):
        self.login()
        data = MultiDict()

        for k in self.attrs:
            data.add(k,self.attrs[k])

        data = ImmutableMultiDict(data)

        response = self.app.post(
            '/artifacts/new',
            data = data,
            headers = {"Content-Type":"application/x-www-form-urlencoded"},
            follow_redirects=True)
        assert "Artifact created" in str(response.data)

    def test_create_source(self):
        self.login()
        data = MultiDict()

        for k in self.attrs:
            data.add(k,self.attrs[k])

        data.add("source_name","source")
        data = ImmutableMultiDict(data)

        response = self.app.post(
            '/artifacts/new',
            data = data,
            headers = {"Content-Type":"application/x-www-form-urlencoded"},
            follow_redirects=True)
        assert "Artifact created" in str(response.data)

if __name__ == '__main__':
    unittest.main()
