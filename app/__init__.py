from flask import Flask # flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt # database stuff

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'user.login' # login stuff

import os # general


bcrypt = Bcrypt()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SECRET_KEY'] = os.urandom(16).hex() # replace this with an actual secret key at some point

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Reduces overhead

    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # blueprints here
    from .base.views import base_blueprint
    app.register_blueprint(base_blueprint, url_prefix='/')
    from .user.views import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')
    from .flashCards.views import flash_cards_blueprint
    app.register_blueprint(flash_cards_blueprint, url_prefix='/flashcards')

    #any login stuff here
    @login_manager.user_loader
    def load_user(user_id):
        from .user.models import User
        return User.query.get(int(user_id))
    return app



    

