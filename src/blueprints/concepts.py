from flask import Blueprint, render_template, request, redirect, url_for
from src.models import Concept
from src import db

concepts_template = Blueprint('concepts', __name__, template_folder='../templates')

@concepts_template.route('/concepts/<concept_id>', methods=["GET"])
def concept(concept_id):
    '''
    View for concept
    '''
    # def put (update)
    # def delete (destroy)
    if request.method == 'GET':
        concept = Concept.query.get(concept_id)
        return render_template('concepts/view.html', concept=concept)
    else:
        return render_template('404.html')

@concepts_template.route('/concepts/new')
def concept_new():
    return render_template('concepts/new.html')
# @concepts_template.route('/concepts')
# def get (list)
# def post (create)

#@concepts_template.route('/concepts/<id>/ edit')
# def get (edit)
