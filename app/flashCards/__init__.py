from flask import Blueprint

flash_cards_blueprint = Blueprint('flash_cards', __name__)

from . import views
from app import create_app
from app import db

app = create_app()

with app.app_context():
    db.create_all()