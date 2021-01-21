from flask import Blueprint, render_template, flash, redirect, request, url_for
from src.models import User
from src.forms import LoginForm, RegistrationForm
from src import db

users_template = Blueprint('users', __name__, template_folder='../templates')
