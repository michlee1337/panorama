from flask import Blueprint, render_template, flash, request, redirect, url_for
from src.models import Studyplan, Concept, Topic, Resource, Reading
from src.helpers import get_or_create
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
        try:
            if request.form['title'] == "" or request.form['about'] == "":
                raise ValueError
            concept = Concept(title=request.form['about'])
            db.session.add(concept)

            studyplan = Studyplan(title=request.form['title'], description=request.form['description'], concept=concept)
            db.session.add(studyplan)

            for prereq in request.form['prerequisites'].split(','):
                prereq_concept = get_or_create(db.session, Concept, title=prereq)
                concept.prerequisites.append(prereq_concept)

            print("DEBUG preq")

            topics = []
            concepts = []

            for topic_name, topic_description in zip(request.form['topics'].split(','), request.form['topic_descriptions'].split(',')):
                if topic_name != "":
                    topic_concept = get_or_create(db.session, Concept, title=topic_name)
                    concept.children.append(topic_concept)
                    concepts.append(topic_concept)  # for adding resources later

                    topic = Topic(concept=topic_concept, description=topic_description, studyplan=studyplan)
                    db.session.add(topic)
                    topics.append(topic)  # for adding readings later
                    studyplan.topics.append(topic)

            # print("DEBUG topic")

            for reading_name, reading_link, reading_description, topic_idx in zip(request.form['reading_names'].split(','), request.form['reading_links'].split(','), request.form['reading_descriptions'].split(','), request.form['readings_to_topic_idx'].split(',')):
                if reading_name != "" and reading_link != "":
                    topic_idx = int(topic_idx)

                    # print("DEBUG resource pre")
                    resource = get_or_create(db.session, Resource, name=reading_name, link=reading_link)
                    resource.concepts.append(concepts[topic_idx])
                    # print("DEBUG resource post")

                    # print("DEBUG reading pre")
                    reading = Reading(resource=resource, description=reading_description)  # DEV: add studyplan details later
                    # print("DEBUG reading post")
                    db.session.add(reading)
                    # print("DEBUG reading sesh")

                    print("DEBUG APPEND", topics[topic_idx], reading, topics[topic_idx].readings)
                    topics[topic_idx].readings.append(reading)
                    print("DEBUG reading append")
            print("DEBUG reading")
            db.session.commit()
            flash('Studyplan created!')
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            print("Exception: ", e)
            flash('Error creating studyplan... sorry!')
            return render_template('studyplans/new.html')

# @studyplans_template.route('/studyplans')
# def get (list)
# def post (create)

#@studyplans_template.route('/studyplans/<id>/ edit')
# def get (edit)
