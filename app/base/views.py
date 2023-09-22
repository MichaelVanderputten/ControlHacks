from flask import render_template, redirect, url_for, Blueprint, request, current_app
from app.__init__ import bcrypt


base_bp = Blueprint('home', __name__)

@base_bp.route('/')
def home():
    return render_template('base/home.html')