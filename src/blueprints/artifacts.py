from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import current_user
from src.models import Artifact, Concept, Chunk
from src.forms import ArtifactForm
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
    if artifact is None:
        flash('Artifact not found.')
        return render_template('pages/index.html')
    return render_template('artifacts/view.html', artifact=artifact)

@artifacts_template.route('/artifacts/new', methods=["GET","POST"])
def new():
    '''
    Creates new artifact

    A GET request will return the appropriate create view.

    A POST request will attempt to create a artifact with the
    provided information, and will flash the raised error upon any failure.
    '''
    if not current_user.is_authenticated:
        flash('Login to contribute!')
        return redirect(url_for('pages.login'))

    fork_id, artifact = request.args.get('fork_id'), None
    if fork_id is not None:
        artifact = Artifact.query.get(fork_id)
        if artifact is None:
            flash('Artifact not found.')

    if request.method == 'GET':
        form = ArtifactForm(obj=artifact)
        return render_template('artifacts/new.html', form=form)
    elif request.method == 'POST':
        form = ArtifactForm(request.form)
        try:
            Artifact(form)
            flash('Artifact created!')
            return redirect('/')
        except Exception as e:
            flash('Error creating artifact... sorry! {}'.format(e))
            return render_template('artifacts/new.html', form=form)

@artifacts_template.route('/artifacts/<artifact_id>/edit',  methods=["GET","POST"])
def edit(artifact_id):
    '''
    edit for artifact

    Only accepts GET requests.
    It gets the appropriate information and passes it to the View.
    '''
    artifact = Artifact.query.get(artifact_id)
    if artifact is None:
        flash('Artifact not found.')
        return render_template('pages/index.html')

    if request.method == 'GET':
        form = ArtifactForm(obj=artifact)
        return render_template('artifacts/edit.html', form=form, artifact=artifact)
    elif request.method == 'POST':
        try:
            form = ArtifactForm(formdata=request.form)
            artifact.save_changes(form)
            flash('Changes saved!')
            return render_template(url_for('artifacts.view', artifact_id=artifact.id))
        except Exception as e:
            flash('Error creating artifact... sorry! {}'.format(e))
            return render_template('artifacts/edit.html', form=form, artifact=artifact)

@artifacts_template.route('/artifacts/search')
def search():
    '''
    Returns index page with only results that have a title that match
    given search parameters

    If no filters are provided, will return artifacts that contain the search
    term in their title.

    If filters are provided, will return artifacts that contain the search term
    and match provided filters.

    Uses Postgres LIKE query to match search terms.

    Accepts filters
        - search by type (text/ video)
        - search by duration (mins, hours, days, months, ?)

    Any search patterns not recognized will be ignored and a warning will flash.
    '''
    return render_template('pages/index.html', artifacts = Artifact.search(request.args))

@artifacts_template.route('/artifacts/by_concept')
def by_concept():
    '''
    Responds to queries for artifacts by concept.

    Only accepts GET requests

    It returns JSON of artifacts that have the relevant concept
    '''
    concept_id = int(request.args.get('concept_id'))
    exclude_id = int(request.args.get('exclude_id'))

    concept = Concept.query.get(concept_id)
    artifacts = []
    for artifact in concept.artifacts:
        if artifact.id != exclude_id:
            artifact_info = {
                'id': artifact.id,
                'title': artifact.title,
                'prerequisites': [p.title for p in artifact.prerequisites],
                'description': artifact.description,
                'chunks': [t.concept.title for t in artifact.chunks]
            }
            artifacts.append(artifact_info)
    return jsonify(artifacts=artifacts)
