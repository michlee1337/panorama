[![Build Status](https://travis-ci.com/michlee1337/panorama.svg?branch=master)](https://travis-ci.com/michlee1337/panorama)

This project is a side project/ experiment. </br>
The objective is as follows:
- support self directed learning via the user journey of figuring out what is the concept you want to learn while searching for resources.
- encourage metacognition by presenting the concept map first and encouraging users to explore/ search in terms of concepts.

See the live website [here](https://panorama-stage.herokuapp.com/artifacts/search) </br>

# Searching for resources
[![Searching for resources](https://img.youtube.com/vi/RwjTc0yDfAc/0.jpg)](https://www.youtube.com/watch?v=RwjTc0yDfAc)
- Find resources by concepts, subconcepts, prerequisites, mediatype, and duration.

# Exploring related concepts
[![Exploring related concepts](https://img.youtube.com/vi/yPmlOpmwDAU/0.jpg)](https://www.youtube.com/watch?v=yPmlOpmwDAU)
- Refine search or explore related resources by exploring foundations (prerequisites), alternatives (same concept), or deep dive (expanding on sub concepts).

# Filestucture
- Loosely follows MVC
- app initialization can be found in `src/__init__.py`
- models can be found in `src/models`
- blueprints can be found in `src/blueprints`
- templates can be found in `src/templates`

# Prerequisites
Install [Python3](https://www.python.org/downloads/)
Set up [Postgresql](https://www.elliotblackburn.com/installing-postgresql-on-macos-osx/)
- create database and set the appropriate database url (elaborated below)
Set up virtual environment
- create `virtualenv src`
- set DATABASE_URL [environment variable](https://stackoverflow.com/questions/9554087/setting-an-environment-variable-in-virtualenv)
- Start `source env/bin/activate`

# Set up Prerequisites
1. Start virtual enviroment `source env/bin/activate`
2. Load requirements: `pip install -r requirements.txt`
3. Run app: `python3 src/__init__.py`

# Dev
**To Upload a Dropbox Dump Database to Heroku**
```heroku pg:backups:restore 'https://dl.dropboxusercontent.com/<random string from dropbox link>/<file name>' DATABASE --app panorama-stage```

**To Update Db**
flask db migrate -m "comment"
flask db upgrade

# Test
1. Start virtual env
2. `python3 -m unittest discover tests`
