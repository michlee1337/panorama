from flask import Blueprint, render_template, request, redirect, url_for
from src.models import Studyplan, Reading
from src import db

pages_template = Blueprint('pages', __name__, template_folder='../templates')

@pages_template.route('/')
def index():
    return render_template('pages/index.html', studyplans = Studyplan.query.all())

@pages_template.route('/search')
def search():
    '''
    Returns index page with only results that have a title that match
    given search parameters

    If no filters are provided, will return studyplans that contain the search
    term in their title.

    If filters are provided, will return readings that contain the search term
    and match provided filters.

    Uses Postgres LIKE query to match search terms.

    Accepts filters
        - search by type (text/ video)
        - search by title
    Any search patterns not recognized will be ignored and a warning will flash.

    '''
    # DEV: This is temporary as future refactoring to have a less awkward divison between
    ## Studyplans and Readings will be done that allows for a search on a shared parent model.

    if (request.args.get('type') != "") or (request.args.get('depth') != ""):
        return render_template('pages/index.html', readings = Reading.getMatchingReadings(request.args))
    else:
        return render_template('pages/index.html', studyplans = Studyplan.getMatching(request.args.get('term')))

# @pages_template.route('/pages')
# def get (list)
# def post (create)

#@pages_template.route('/pages/<id>/ edit')
# def get (edit)
