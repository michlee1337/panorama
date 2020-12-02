from flask import Blueprint, render_template, request, redirect, url_for
from src.models import Studyplan
from src import db

pages_template = Blueprint('pages', __name__, template_folder='../templates')

@pages_template.route('/')
def index():
    return render_template('pages/index.html', studyplans = Studyplan.query.all())
# @pages_template.route('/pages')
# def get (list)
# def post (create)

#@pages_template.route('/pages/<id>/ edit')
# def get (edit)
