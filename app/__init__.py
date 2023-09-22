from flask import Flask # flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt# database stuff

import os # general


def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SECRET_KEY'] = os.urandom(16).hex() # replace this with an actual secret key at some point

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Reduces overhead

    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # blueprints here

    #any login stuff here

    return app


bcrypt = Bcrypt()

db = SQLAlchemy()
migrate = Migrate()