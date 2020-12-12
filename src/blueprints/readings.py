from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from src.models import Studyplan, Concept, Topic, Resource, Reading
from src import db

readings_template = Blueprint('readings', __name__, template_folder='../templates')

@readings_template.route('/readings/concept')
def readings_by_concept():
    '''
    Returns JSON of readings that have the relevant concept
    '''
    concept_id = int(request.args.get('concept_id'))

    concept = Concept.query.get(concept_id)
    readings = []
    for resource in concept.resources:
        # get top reading
        reading = resource.readings[0]
        reading_info = {
            'id': reading.id,
            'name': resource.name,
            'link': resource.link,
            'description': reading.description,
        }
        readings.append(reading_info)
    return jsonify(readings=readings)
