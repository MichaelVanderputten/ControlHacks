from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_required

from .forms import CreateDeckForm
from .models import Deck, FlashCard
from app import db

from . import flash_cards_blueprint # blueprint

@flash_cards_blueprint.route('/home')
@login_required
def home():
    return render_template('flashCards/home.html')

@flash_cards_blueprint.route('/create')
@login_required
def createFC():
    return render_template('flashCards/createFC.html')

@flash_cards_blueprint.route('/create_deck', methods=['GET', 'POST'])
def create_deck():
    form = CreateDeckForm()
    if form.validate_on_submit():
        new_deck = Deck(
            name=form.name.data,
            private=form.private.data,
            creator_id=1  # Replace this later with logged-in user ID
        )
        db.session.add(new_deck)
        db.session.flush()

        num_cards = form.num_cards.data
        flash_cards = []

        for i in range(1, num_cards + 1):
            question = request.form.get(f'question{i}')
            answer = request.form.get(f'answer{i}')

            if question and answer:
                flash_card = FlashCard(
                    question=question, 
                    answer=answer, 
                    deck_id=new_deck.id, 
                    creator_id=1
                )
                flash_cards.append(flash_card)

        db.session.add_all(flash_cards)
        db.session.commit()

        flash('New deck and flashcards created successfully.')
        return redirect(url_for('index'))

    return render_template('create_deck.html', form=form)

