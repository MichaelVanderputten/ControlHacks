from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required

from . import flash_cards_blueprint # blueprint

@flash_cards_blueprint.route('/home')
@login_required
def home():
    return render_template('flashCards/home.html')

