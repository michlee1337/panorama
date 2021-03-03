from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user
from src.models.users import User
from src.models.artifacts import Artifact
from src.forms import LoginForm, RegistrationForm

from src.models import db

pages_template = Blueprint('pages', __name__, template_folder='../templates')

@pages_template.route('/')
def index():
    artifacts = Artifact.query.all()

    return render_template('pages/index.html', artifacts=artifacts)

@pages_template.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login

    A GET request will redirect to the login view.

    A POST request will check for valid login data.
    Valid login data requires existing user instance with
    matching username, password, and email.
    Success/ failure will result in redirect to homepage/ login respectively.
    """
    form = LoginForm()
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return render_template('pages/login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('pages.login'))
            login_user(user)
            flash('Logged in successfully.')
            return redirect('/')
        else:
            flash('Provided login details not recognized.')
            return render_template('pages/login.html', form=form)

@pages_template.route('/logout')
def logout():
    """
    User logout

    It will attempt to logout user if it exists and redirect to the homepage.
    """
    logout_user()
    return redirect('/')

@pages_template.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration

    A GET request will redirect to the register view.

    A POST request will check that the user is not currently logged in,
    afterwards it will create a new user based on provided data and redirect
    to homepage.

    Any form input validation (ex: must not be empty) is done in the application logic,
    visible in /src/forms.py
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('pages.login'))
    return render_template('pages/register.html', title='Register', form=form)
