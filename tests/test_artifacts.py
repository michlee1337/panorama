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
            "duration":"0"}

    def test_require_title(self):
            self.app.post('login', data = dict(email="example@gmail.com", username="example", password="111"), follow_redirects=True)
            response = self.app.post(
                '/artifacts/new',
                data = dict(main_concept="111"),
                headers = {"Content-Type":"application/x-www-form-urlencoded"})
            assert "Title and Main Concept is required" in str(response.data)

    def test_require_concept(self):
            self.app.post('login', data = dict(email="example@gmail.com", username="example", password="111"), follow_redirects=True)
            response = self.app.post(
                '/artifacts/new',
                data = dict(title="111"),
                headers = {"Content-Type":"application/x-www-form-urlencoded"})
            assert "Title and Main Concept is required" in str(response.data)

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

    def test_create_prereqs(self):
        self.login()
        data = MultiDict()

        for k in self.attrs:
            data.add(k,self.attrs[k])

        data.add("prereqs[]","concept1")
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

    def test_create_chunks(self):
        self.login()
        data = MultiDict()

        for k in self.attrs:
            data.add(k,self.attrs[k])

        data.add("chunk_titles[]", "chunk_title")
        data.add("chunk_concepts[]", "chunk_concept")
        data.add("chunk_contents[]", "chunk_content")

        data = ImmutableMultiDict(data)

        response = self.app.post(
            '/artifacts/new',
            data = data,
            headers = {"Content-Type":"application/x-www-form-urlencoded"},
            follow_redirects=True)
        assert "Artifact created" in str(response.data)

    def test_create_chunks_malformed(self):
        self.login()
        data = MultiDict()

        for k in self.attrs:
            data.add(k,self.attrs[k])

        data.add("chunk_titles[]", "chunk_title")
        data.add("chunk_contents[]", "chunk_content")

        data = ImmutableMultiDict(data)

        response = self.app.post(
            '/artifacts/new',
            data = data,
            headers = {"Content-Type":"application/x-www-form-urlencoded"},
            follow_redirects=True)
        assert "Chunk data is malformed" in str(response.data)

    def test_create_unrecognized_mediatype(self):
        self.login()
        data = MultiDict()

        for k in self.attrs:
            data.add(k,self.attrs[k])

        data.setlist("mediatype", ["5"])

        data = ImmutableMultiDict(data)

        response = self.app.post(
            '/artifacts/new',
            data = data,
            headers = {"Content-Type":"application/x-www-form-urlencoded"},
            follow_redirects=True)
        assert "Mediatype is not recognized" in str(response.data)

    def test_create_unrecognized_duration(self):
        self.login()
        data = MultiDict()

        for k in self.attrs:
            data.add(k,self.attrs[k])

        data.setlist("duration", ["5"])

        data = ImmutableMultiDict(data)

        response = self.app.post(
            '/artifacts/new',
            data = data,
            headers = {"Content-Type":"application/x-www-form-urlencoded"},
            follow_redirects=True)
        assert "Duration is not recognized" in str(response.data)

if __name__ == '__main__':
    unittest.main()
