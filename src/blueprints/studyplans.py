from flask import Blueprint, render_template, request, redirect, url_for
from src.models import StudyPlan
from src import db

studyplans_template = Blueprint('studyplans', __name__, template_folder='../templates')

@studyplans_template.route('/studyplans/<studyplan_id>', methods=["GET"])
def studyplan(studyplan_id):
    '''
    View for studyplan
    '''
    if request.method == 'GET':
        studyplan = Concept.query.get(studyplan_id)
        return render_template('studyplans/view.html', studyplan=studyplan)
    else:
        return render_template('404.html')

@studyplans_template.route('/studyplans/new')
def studyplan_new():
    return render_template('studyplans/new.html')
# @studyplans_template.route('/studyplans')
# def get (list)
# def post (create)

#@studyplans_template.route('/studyplans/<id>/ edit')
# def get (edit)
