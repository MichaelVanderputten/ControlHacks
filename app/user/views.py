from flask import render_template, redirect, url_for, Blueprint, request, current_app, flash # flask

from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash # login stuff

from app.user.forms import RegistrationForm
from app.user.forms import LoginForm
from app.user.models import User 
from app import db
from app.__init__ import bcrypt # app stuff

from . import user_blueprint # blueprint

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(first_name=form.first_name.data).first()  # Changed from email to first_name
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('flash_cards.home'))  # login success
        else:
            flash('Login Unsuccessful. Please check first name and password', 'danger')  # Changed from email to first name
    return render_template('user/login.html', title='Login', form=form)

@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('base.aboutUs'))

@user_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    #db = current_app.extensions['sqlalchemy'].DB

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            display_name=form.display_name.data,
            password_hash=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', title='Register', form=form)