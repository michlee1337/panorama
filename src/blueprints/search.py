from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from src.models import Studyplan, Concept, Topic, Resource, Reading
from src import db

search_template = Blueprint('search', __name__, template_folder='../templates')

@search_template.route('/search/')
def full_text_search():
    '''
    Returns JSON of studyplans and resources that match search query ordered by similarity.

    Expects two parameters:
        - search keys [comma seperated string]
        - search terms [comma seperated string]
    Uses postgresql LIKE query to match anything that contains the term.

    Search patterns accepted currently:
        - search by type (studyplan/ resource)
        - search by title
        - search by description

    Any search patterns not recognized will be ignored and a warning will flash.
    '''
    search_keys = request.args.get('search_keys').split(",")
    search_terms = request.args.get('search_terms').split(",")

    if len(search_keys) == 0:
        flash("Please provide a search term")
        return

    # DEV: look for a cleaner way to do this
    ## Current method: SQL statements for maintainence
    filter_terms = {"title", "description"}
    seen_keys = {}  # ensure no duplicate keys
    filter_sql = ""

    for key, term in zip(search_keys, search_terms):
        if key in seen_keys:
            flash("Search term duplicated. Only first instance considered.")
        elif key == "type":
            pass
        elif key in filter_terms:
            if filter_sql == "":
                filter_sql = "WHERE {} LIKE %{}%".format(key, term)
            else:
                filter_sql += ("AND {} LIKE %{}%".format(key, term))
        else:
            flash("Search term not recognized and ignored")

    studyplans_res = []
    resources_res = []

    # handle type filter
    try:
        type_idx = search_keys.index("type")
        if search_terms[type_idx] == "studyplan":
            studyplans_res = db.engine.execute("SELECT * FROM studyplans" + filter_sql)
        elif search_terms[type_idx] == "resources":
            resources_res = db.engine.execute("SELECT * FROM resources" + filter_sql)
        else:
            flash("Type not recognized and ignored")
    except ValueError:
        studyplans_res = db.engine.execute("SELECT * FROM studyplans" + filter_sql)
        resources_res = db.engine.execute("SELECT * FROM resources" + filter_sql)
    print("DEBUG", [r[0] for r in studyplans_res], [r[0] for r in resources_res])
    return
#     cur_search_id = int(request.args.get('cur_search_id'))
#
#     concept = Concept.query.get(concept_id)
#     search = []
#     for search in concept.search:
#         if search.id != cur_search_id:
#             search_info = {
#                 'id': search.id,
#                 'title': search.title,
#                 'prerequisites': [p.title for p in search.concept.prerequisites],
#                 'description': search.description,
#                 'topics': [t.concept.title for t in search.topics]
#             }
#             search.append(search_info)
#     return jsonify(search=search)
# #tag = request.form["tag"]
# search = "%{}%".format(tag)
# posts = Post.query.filter(Post.tags.like(search)).all()
#
# @search_template.route('/search')
# def get (list)
# def post (create)

#@search_template.route('/search/<id>/ edit')
# def get (edit)
