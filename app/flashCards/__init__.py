from flask import Blueprint

flash_cards_blueprint = Blueprint('flash_cards', __name__)

from . import views
