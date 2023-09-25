from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required


from .forms import CreateDeckForm, CreateFlashCards
from .models import Deck, FlashCard
from app import db

from app.base.views import get_top_users, update_forced, check_daily


from . import flash_cards_blueprint # blueprint


@flash_cards_blueprint.route('/home')
@login_required
def home():
   check_daily()
   print_decks()

   user_details = { # spacific details
        'streek': current_user.streek,
        'points': current_user.points,
        'multiplier': current_user.point_multiplier
    }

   allDecks = Deck.query.all()
   return render_template('flashCards/home.html', allDecks = allDecks, user_details=user_details
      )


@flash_cards_blueprint.route('/view_Deck/<int:deck_id>')
@login_required
def view_Deck(deck_id):
   deck = Deck.query.get_or_404(deck_id)
   flashcards = deck.flashCard
   return render_template('view_deck.html', deck=deck, flashcards=flashcards)# use this to diplay the correct set of flash cards



@flash_cards_blueprint.route('/create_deck', methods=['GET', 'POST'])
@login_required
def create_deck():
   form = CreateDeckForm()
   if form.validate_on_submit():
       deck = Deck(
           name=form.name.data,
           private=form.private.data,
           creator_id=1  # Replace this later with logged-in user ID
       )
       db.session.add(deck)
       db.session.flush()
       db.session.commit()

       return redirect(url_for('flash_cards.home'))
  
   return render_template('flashCards/create_deck.html', form=form)# creates a new deck


@flash_cards_blueprint.route('/create_Flash_Cards/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def create_Flash_Cards(deck_id):
   deck = Deck.query.get_or_404(deck.id)
   form = CreateFlashCards()
   if form.validate_on_submit():
       flashCard = FlashCard(
           question = form.question.data,
           answer = form.answer.data,
           deck_id= deck.id
   )
       db.session.add(flashCard)
       db.session.commit()
       flash('Flash card successfully added to the deck')

       return redirect(url_for('flash_cards.view_deck', deck_id = deck_id))
  
   return render_template('flashCards/createFC.html', form = form)# this def creates new flashcards in the set selected

def print_decks():
    all_decks = Deck.query.all()
    for deck in all_decks:
        print(f"Deck ID: {deck.id}, Deck Name: {deck.name}, Creator ID: {deck.creator_id}")