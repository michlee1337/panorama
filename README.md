This project is a WIP. </br>
View the latest production code [here](https://panorama-pro.herokuapp.com/).

# Reqs
Postgresql
https://www.elliotblackburn.com/installing-postgresql-on-macos-osx/

# Run
0. Install [Python3](https://www.python.org/downloads/)
1. Start pip env: `source env/bin/activate`
2. Run app: `python3 src/__init__.py`

# Dev
**To Upload a Dropbox Dump Database to Heroku**
``` heroku pg:backups:restore 'https://dl.dropboxusercontent.com/<random string from dropbox link>/<file name>' DATABASE --app panorama-stage```
