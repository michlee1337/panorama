from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from src.models import Studyplan, Concept, Topic, Resource, Reading
from src import db

studyplans_template = Blueprint('studyplans', __name__, template_folder='../templates')

@studyplans_template.route('/studyplans/<studyplan_id>', methods=["GET"])
def view(studyplan_id):
    '''
    View for studyplan
    '''
    if request.method == 'GET':
        studyplan = Studyplan.query.get(studyplan_id)
        return render_template('studyplans/view.html', studyplan=studyplan)
    else:
        return render_template('404.html')

@studyplans_template.route('/studyplans/new', methods=["GET","POST"])
def studyplan_new():
    if request.method == 'GET':
        return render_template('studyplans/new.html')
    elif request.method == 'POST':
        try:
            Studyplan.create(request.form)
            flash('Studyplan created!')
            return redirect('/')
        except Exception as e:
            print("DEBUG: ", e)
            flash('Error creating studyplan... sorry!')
            return render_template('studyplans/new.html')

@studyplans_template.route('/studyplans')
def studyplans_about_concept():
    '''
    Returns JSON of studyplans that have the relevant concept
    '''
    concept_id = request.args.get('concept_id')
    concept = Concept.query.get(concept_id)
    studyplans = []
    for studyplan in concept.studyplans:
        print("HELLO")
        studyplan = {
            'id': studyplan.id,
            'title': studyplan.title,
            'prerequisites': [p.title for p in studyplan.concept.prerequisites],
            'description': studyplan.description,
            'topics': [t.concept.title for t in studyplan.topics]
        }
        studyplans.append(studyplan)
    return jsonify(studyplans=studyplans)
# @studyplans_template.route('/studyplans')
# def get (list)
# def post (create)

#@studyplans_template.route('/studyplans/<id>/ edit')
# def get (edit)
