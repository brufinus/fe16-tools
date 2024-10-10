from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

def get_choices(table):
    result_list = []
    rows = table.query.order_by(table.name.asc()).all()
    for row in rows:
        tup = (row.id, row.name)
        result_list.append(tup)
    return result_list

class DualCharacterForm(FlaskForm):
    character1 = SelectField('Character 1', choices=[], render_kw={'autofocus': True, 'id': 'dropdown1'})
    character2 = SelectField('Character 2', choices=[], render_kw={'id': 'dropdown2'})

class CharacterForm(FlaskForm):
    character = SelectField('Character', choices=[], render_kw={'autofocus': True, 'id': 'dropdown'})

class ItemForm(FlaskForm):
    lost_item = SelectField('Item', choices=[], render_kw={'autofocus': True, 'id': 'lost_item_dropdown'})
    character = SelectField('Character', choices=[], render_kw={'id': 'character_dropdown'})

class SeedForm(FlaskForm):
    seed = SelectField('Seed', choices=[], render_kw={'autofocus': True, 'id': 'seed_dropdown'})
