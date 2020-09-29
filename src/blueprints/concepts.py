from flask import Blueprint, render_template, request, redirect, url_for
from src.models import Concept
from src import db

concepts_template = Blueprint('concepts', __name__, template_folder='../templates')

@concepts_template.route('/concepts/<concept_id>')
def view_concept(concept_id):
    '''
    View for concept
    '''
    concept = Concept.query.get(concept_id)

    return render_template('view_concept.html', concept=concept)
