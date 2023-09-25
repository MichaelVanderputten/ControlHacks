from flask import Blueprint

base_blueprint = Blueprint('base', __name__)

from . import views