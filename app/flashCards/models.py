from datetime import datetime
from app import db
from app.user.models import User

class Deck(db.Model):
    __tablename__ = 'deck'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    private = db.Column(db.Boolean, default=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)

    flash_cards = db.relationship('FlashCard', backref='deck', lazy=True)
    creator = db.relationship('User', backref='decks')


class FlashCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(256), nullable=False)
    answer = db.Column(db.String(256), nullable=False)
    
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)

    creator = db.relationship('User', backref='flash_cards')

    def __repr__(self):
        return f'<FlashCard {self.question}>'


def init_db():
    db.create_all()

    # Create a test deck
    #deck = Deck('name',)
    #new_user.display_name = 'Nathan'
    #db.session.add(new_user)
    #db.session.commit()

    #new_user.datetime_subscription_valid_until = datetime.datetime(2019, 1, 1)
    db.session.commit()


if __name__ == '__main__':
    init_db()