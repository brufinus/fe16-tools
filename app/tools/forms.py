from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField


class CharacterForm(FlaskForm):
    character = SelectField('Character', choices=[], render_kw={'autofocus': True, 'id': 'dropdown'})

class DualCharacterForm(FlaskForm):
    character1 = SelectField('Character 1', choices=[], render_kw={'autofocus': True, 'id': 'dropdown1'})
    character2 = SelectField('Character 2', choices=[], render_kw={'id': 'dropdown2'})

class ItemForm(FlaskForm):
    lost_item = SelectField('Item', choices=[], render_kw={'autofocus': True, 'id': 'lost_item_dropdown'})
    character = SelectField('Character', choices=[], render_kw={'id': 'character_dropdown'})
