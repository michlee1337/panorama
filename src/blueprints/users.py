from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from src.models import User
from src.forms import LoginForm, RegistrationForm
from src import db

users_template = Blueprint('users', __name__, template_folder='../templates')


@users_template.route('/login', methods=['GET', 'POST'])
def login():
    """Page for login"""
    form = LoginForm()
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return render_template('users/login.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            print("VALIDATED")
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('users.login'))
            login_user(user)
            flash('Logged in successfully.')
            return redirect('/')
        else:
            flash('Provided login details not recognized.')
            return render_template('users/login.html', form=form)

@users_template.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@users_template.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)
