from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import current_user
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
        concept_ids = [t.concept.id for t in studyplan.topics]
        return render_template('studyplans/view.html', studyplan=studyplan, concept_ids=concept_ids)
    else:
        return render_template('404.html')

@studyplans_template.route('/studyplans/new', methods=["GET","POST"])
def new():
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
            flash('Error creating studyplan... sorry!')
            return render_template('studyplans/new.html')

@studyplans_template.route('/studyplans/concept')
def studyplans_by_concept():
    '''
    Returns JSON of studyplans that have the relevant concept
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

# @studyplans_template.route('/studyplans/title')
# def studyplans_by_title():
#     '''
#     Returns JSON of studyplans that have the relevant term in title
#
#     Uses Postgres LIKE query to match anything that contains the search term
#     '''
#     term = request.args.get('term')
#
#     studyplans = Studyplan.query.filter(Studyplan.title.contains(term)).all()
#     json_studyplans = []
#
#     for studyplan in studyplans:
#         studyplan_info = {
#             'id': studyplan.id,
#             'title': studyplan.title,
#             'prerequisites': [p.title for p in studyplan.concept.prerequisites],
#             'description': studyplan.description,
#             'topics': [t.concept.title for t in studyplan.topics]
#         }
#         json_studyplans.append(studyplan_info)
#     return jsonify(studyplans=json_studyplans)
#
#@studyplans_template.route('/studyplans/<id>/ edit')
# def get (edit)
