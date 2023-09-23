from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class CreateDeckForm(FlaskForm):
    name = StringField('Deck Name', validators=[DataRequired()])
    creator = StringField('Creator Name', validators=[DataRequired()])
    private = BooleanField('Private')
    num_cards = IntegerField('Number of Cards', validators=[DataRequired()])
    submit = SubmitField('Create Deck')


class CreateFlashCards(FlaskForm):
   question = StringField('question', validators = [DataRequired()])
   answer = StringField('answer', validators = [DataRequired()])
   submit = SubmitField('Create flashCard')
