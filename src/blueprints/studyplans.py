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

@studyplans_template.route('/studyplans/new', methods=["GET","POST"])
def studyplan_new():
    if request.method == 'GET':
        return render_template('studyplans/new.html')
    elif request.method == 'POST':
        # request.form
        # start transaction
        # validate that title and all are there
        # create topics

        # create readings

        # create study plan

        # add relationships

        # jsdata = request.form['javascript_data']
        # data = json.loads(jsdata)[0]
        return

# @studyplans_template.route('/studyplans')
# def get (list)
# def post (create)

#@studyplans_template.route('/studyplans/<id>/ edit')
# def get (edit)
