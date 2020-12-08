from flask import Blueprint, render_template, request, redirect, url_for
from src.models import Studyplan
from src import db

pages_template = Blueprint('pages', __name__, template_folder='../templates')

@pages_template.route('/')
def index():
    return render_template('pages/index.html', studyplans = Studyplan.query.all())

@pages_template.route('/search')
def search():
    '''
    Returns index page with only studyplans that have a title that contains
    the given search term

    Uses Postgres LIKE query to match anything that contains the search term
    '''
    term = request.args.get('term')

    studyplans = Studyplan.query.filter(Studyplan.title.contains(term)).all()

    return render_template('pages/index.html', studyplans = studyplans)


# @pages_template.route('/pages')
# def get (list)
# def post (create)

#@pages_template.route('/pages/<id>/ edit')
# def get (edit)
