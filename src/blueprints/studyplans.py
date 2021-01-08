from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import current_user
from src.models import Artifact, Concept, Chunk
from src import db

artifacts_template = Blueprint('artifacts', __name__, template_folder='../templates')

@artifacts_template.route('/artifacts/<artifact_id>')
def view(artifact_id):
    '''
    View for artifact

    Only accepts GET requests.
    It gets the appropriate information and passes it to the View.
    '''
    artifact = Artifact.query.get(artifact_id)
    concept_ids = artifact.getConcepts()
    return render_template('artifacts/view.html', artifact=artifact, concept_ids=concept_ids)

@artifacts_template.route('/artifacts/new', methods=["GET","POST"])
def new():
    '''
    Creates new artifact

    A GET request will return the appropriate create view.

    A POST request will attempt to create a artifact with the
    provided information, and will flash the raised error upon any failure.
    '''

    if request.method == 'GET':
        if current_user.is_authenticated:
            return render_template('artifacts/new.html')
        else:
            return redirect(url_for('users.login'))
    elif request.method == 'POST':
        try:
            Artifact.create(request.form)
            flash('Artifact created!')
            return redirect('/')
        except Exception as e:
            print("DEBUG: ", e)
            flash('Error creating artifact... sorry! {}'.format(e))
            return render_template('artifacts/new.html')

@artifacts_template.route('/artifacts/concept')
def artifacts_by_concept():
    '''
    Responds to queries for artifacts by concept.

    Only accepts GET requests

    It returns JSON of artifacts that have the relevant concept
    '''
    concept_id = int(request.args.get('concept_id'))
    cur_artifact_id = int(request.args.get('cur_artifact_id'))

    concept = Concept.query.get(concept_id)
    artifacts = []
    for artifact in concept.artifacts:
        if artifact.id != cur_artifact_id:
            artifact_info = {
                'id': artifact.id,
                'title': artifact.title,
                'prerequisites': [p.title for p in artifact.concept.prerequisites],
                'description': artifact.description,
                'chunks': [t.concept.title for t in artifact.chunks]
            }
            artifacts.append(artifact_info)
    return jsonify(artifacts=artifacts)
