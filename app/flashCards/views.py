from flask import render_template, redirect, url_for, flash, request, current_app, Response
from flask_login import current_user, login_required
import requests
import pdfplumber
import io, re

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet



from .forms import CreateDeckForm, CreateFlashCards
from .models import Deck, FlashCard
from app import db

from app.base.views import get_top_users, update_forced, check_daily


from . import flash_cards_blueprint # blueprint

API_URL_LIST = [
    "https://api-inference.huggingface.co/models/Michael-Vptn/text-summarization-t5-base", # michael's text sum model
    "https://api-inference.huggingface.co/models/Michael-Vptn/text-summarization-t5-base",
    "https://api-inference.huggingface.co/models/Michael-Vptn/text-summarization-t5-base",
    "https://api-inference.huggingface.co/models/Michael-Vptn/text-summarization-t5-base",
    "https://api-inference.huggingface.co/models/Michael-Vptn/text-summarization-t5-base",
]

headers = {"Authorization": "Bearer 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"} # hash out on github

global_input_text = ""
global_output_text = "" # api stuff


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

   all_decks = Deck.query.all()
   return render_template('flashCards/home.html', all_decks = all_decks, user_details=user_details
      )


@flash_cards_blueprint.route('/view_Deck/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def view_Deck(deck_id):
   deck = Deck.query.get_or_404(deck_id)
   flashcards = deck.flash_cards

   global global_output_text
   try:
        global global_input_text  # Use the global_input_text variable
        input_text = global_input_text
        output_text = ""

        if request.method == 'POST':
            input_text = request.form['input_text']
            print(input_text)

            output_text = generate(input_text)
            global_output_text = output_text

            print(output_text)

   except Exception as e:
        input_text = ""
        output_text = "An error has occoured. please try again"
        print(f"Main error: {e}")  # Print specific main error to console
   return render_template('flashCards/view_deck.html', deck=deck, flashcards=flashcards, output_text=output_text, input_text=input_text)# use this to diplay the correct set of flash cards

@flash_cards_blueprint.route('/create_deck', methods=['GET', 'POST'])
@login_required
def create_deck():
   form = CreateDeckForm()
   if form.validate_on_submit():
       deck = Deck(
           name=form.name.data,
           private=form.private.data,
           creator_id=current_user.id
       )
       db.session.add(deck)
       db.session.flush()
       db.session.commit()

       return redirect(url_for('flash_cards.home'))
  
   return render_template('flashCards/create_deck.html', form=form)# creates a new deck


@flash_cards_blueprint.route('/create_Flash_Cards/<int:deck_id>', methods=['GET', 'POST'])
@login_required
def create_Flash_Cards(deck_id):

   form = CreateFlashCards()
   if form.validate_on_submit():
       flashCard = FlashCard(
           question = form.question.data,
           answer = form.answer.data,
           deck_id= deck_id,
           creator_id=current_user.id
   )
       db.session.add(flashCard)
       db.session.commit()
       flash('Flash card successfully added to the deck')

       return redirect(url_for('flash_cards.view_Deck', deck_id = deck_id))
  
   return render_template('flashCards/createFC.html', form = form)# this def creates new flashcards in the set selected

def print_decks():
     all_decks = Deck.query.all()
     for deck in all_decks:
       print(f"Deck ID: {deck.id}, Deck Name: {deck.name}, Creator ID: {deck.creator_id}")# debug

def divide(input_str, num):
  # Use regular expression to find sentence breaks
  sentence_breaks = [0] + [
    match.end() for match in re.finditer(r'[.!?]\s+', input_str)
  ]
  total_sentences = len(sentence_breaks)

  # Calculate the indices for dividing the sentences
  indices = [
    sentence_breaks[int(total_sentences * i / num)] for i in range(1, num)
  ]

  # Divide the input string into sentences
  strings = []
  start_index = 0
  for index in indices:
    strings.append(input_str[start_index:index])
    start_index = index

  strings.append(input_str[start_index:])  # Add the remaining part
  return strings

def combine(str_list, bullet_type='bullet'):
  if bullet_type == 'bullet':
    bullet = "• \n"
  elif bullet_type == 'number':
    bullet = "1. "
  else:
    bullet = "- "

  combined = "\n".join([f"{bullet}{item}" for item in str_list])
  return combined

@flash_cards_blueprint.route('/delete_FlashCard/<int:flashcard_id>/<int:deck_id>', methods=['POST'])
@login_required
def delete_FlashCard(flashcard_id, deck_id):
    flashCard = FlashCard.query.get_or_404(flashcard_id)
    if flashCard.deck_id != deck_id:
        flash('You cannot delete this flashcard', 'danger')
        return redirect(url_for('flash_cards.view_Deck', deck_id=deck_id))

    db.session.delete(flashCard)
    db.session.commit()
    flash('FlashCard deleted', 'success')
    return redirect(url_for('flash_cards.view_Deck', deck_id=deck_id))

def generate(input_text):
  try:
    if len(input_text) > 500:

      input_strings = divide(input_text, len(API_URL_LIST))
      output_segments = [
      ]  # List to store generated text segments from different APIs

      for i in range(len(API_URL_LIST)):
        segment = query({"inputs": input_strings[i]}, API_URL_LIST[i])

        output_segments.append(segment[0]["generated_text"])

        output_text = combine(
          output_segments)  # Combine generated text segments
    else:
      output_text = query(
        {"inputs": input_text},
        API_URL_LIST[0])  # if input is too short, only use one api

      output_text = output_text[0]["generated_text"]

    return output_text
  except Exception as e:
    print(f"generate text error: {e}")
    return "Error: text failed to generate. please try again"


def query(payload, API):  # query payload to APIs
  response = requests.post(API, headers=headers, json=payload)
  return response.json()

@flash_cards_blueprint.route('/upload/<int:deck_id>', methods=['POST'])
def upload_file(deck_id):
  try:
    global global_input_text  # Use the global_input_text variable
    if 'pdf_file' in request.files:
      pdf_file = request.files['pdf_file']

      if pdf_file.filename != '':
        with pdfplumber.open(pdf_file) as pdf:
          pdf_text = "\n".join([page.extract_text() for page in pdf.pages])
        global_input_text = pdf_text  # Save the uploaded PDF text to the global variable

  except Exception as e:
    global_input_text = "OH NO! An error has occoured with our PDF upload system. Please try again later! -cozycornbreads"
    print(f"PDF Upload error: {e}")

  return redirect(url_for('flash_cards.view_Deck', deck_id=deck_id))


def generate_pdf(output_text, file_path):
  doc = SimpleDocTemplate(file_path, pagesize=letter)
  styles = getSampleStyleSheet()

  content = []
  content.append(Paragraph("Generated Summary:", styles['Title']))

  # Add the output_text to the PDF
  content.append(Spacer(1, 12))
  content.append(Paragraph(output_text, styles['Normal']))

  doc.build(content)


@flash_cards_blueprint.route('/export_to_pdf')
def export_to_pdf():
  try:
    global global_input_text
    global output_text
    output_text = global_output_text  # Generate the output_text without passing any arguments

    # Create an in-memory PDF file
    pdf_buffer = io.BytesIO()
    generate_pdf(output_text, pdf_buffer)
    pdf_buffer.seek(0)

    # Create a Flask Response with the PDF file
    return Response(
      pdf_buffer.read(),
      content_type='application/pdf',
      headers={'Content-Disposition': 'inline; filename=summary.pdf'})
  except Exception as e:
    error_message = str(e)  # Convert the exception to a string
    print("Export to PDF error:", error_message)
    return f"An error occurred while exporting to PDF: {error_message}"