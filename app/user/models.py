from datetime import datetime, date
from app import db
from app import bcrypt
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=True)
    display_name = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

    points = db.Column(db.Integer, default=0)
    point_multiplier = db.Column(db.Integer, default=1)

    last_visited = db.Column(db.Date)
    streek = db.Column(db.Integer, default=1)


    def __repr__(self):
        return f'<User {self.display_name}>'
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)