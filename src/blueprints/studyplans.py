from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import current_user
from src.models import Studyplan, Concept, Topic, Resource, Reading
from src import db

studyplans_template = Blueprint('studyplans', __name__, template_folder='../templates')

@studyplans_template.route('/studyplans/<studyplan_id>')
def view(studyplan_id):
    '''
    View for studyplan

    Only accepts GET requests.
    It gets the appropriate information and passes it to the View.
    '''
    studyplan = Studyplan.query.get(studyplan_id)
    concept_ids = studyplan.getConcepts()
    return render_template('studyplans/view.html', studyplan=studyplan, concept_ids=concept_ids)

@studyplans_template.route('/studyplans/new', methods=["GET","POST"])
def new():
    '''
    Creates new studyplan

    A GET request will return the appropriate create view.

    A POST request will attempt to create a studyplan with the
    provided information, and will flash the raised error upon any failure.
    '''

    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('studyplans/new.html')
        else:
            return redirect(url_for('users.login'))
    elif request.method == 'POST':
        try:
            Studyplan.create(request.form)
            flash('Studyplan created!')
            return redirect('/')
        except Exception as e:
            print("DEBUG: ", e)
            flash('Error creating studyplan... sorry! {}'.format(e))
            return render_template('studyplans/new.html')

@studyplans_template.route('/studyplans/concept')
def studyplans_by_concept():
    '''
    Responds to queries for studyplans by concept.

    Only accepts GET requests

    It returns JSON of studyplans that have the relevant concept
    '''
    concept_id = int(request.args.get('concept_id'))
    cur_studyplan_id = int(request.args.get('cur_studyplan_id'))

    concept = Concept.query.get(concept_id)
    studyplans = []
    for studyplan in concept.studyplans:
        if studyplan.id != cur_studyplan_id:
            studyplan_info = {
                'id': studyplan.id,
                'title': studyplan.title,
                'prerequisites': [p.title for p in studyplan.concept.prerequisites],
                'description': studyplan.description,
                'topics': [t.concept.title for t in studyplan.topics]
            }
            studyplans.append(studyplan_info)
    return jsonify(studyplans=studyplans)
