from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

def get_choices(character):
    char_list = []
    chars = character.query.order_by(character.name.asc()).all()
    for char in chars:
        tup = (char.id, char.name)
        char_list.append(tup)
    return char_list

class CharacterForm(FlaskForm):
    char_list = []
    character1 = SelectField('Character 1', choices=[], render_kw={'autofocus': True, 'id': 'dropdown1'})
    character2 = SelectField('Character 2', choices=[], render_kw={'id': 'dropdown2'})