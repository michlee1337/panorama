This project is a WIP. </br>
View the latest production code [here](https://panorama-pro.herokuapp.com/). </br>
View this [demo video](https://www.loom.com/share/99ebf66f2c13421ea1cc5d23f741786f?sharedAppSource=personal_library) for an overview of current functionality.

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
