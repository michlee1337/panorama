from flask import Blueprint, render_template, request, redirect, url_for
# from src.models import Artifact
from src import db

pages_template = Blueprint('pages', __name__, template_folder='../templates')

@pages_template.route('/')
def index():
    return render_template('pages/index.html')
