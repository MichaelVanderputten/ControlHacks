from flask import render_template, redirect, url_for, Blueprint, request, current_app
from app.__init__ import bcrypt


from . import base_blueprint # blueprint

@base_blueprint.route('/aboutUs')
def aboutUs():
    return render_template('base/aboutUs.html')