from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField


class CharacterForm(FlaskForm):
    character = SelectField('Character', choices=[], render_kw={'autofocus': True, 'id': 'dropdown'})

class DualCharacterForm(FlaskForm):
    character1 = SelectField('Character 1', choices=[], render_kw={'autofocus': True, 'id': 'dropdown1'})
    character2 = SelectField('Character 2', choices=[], render_kw={'id': 'dropdown2'})

class ItemForm(FlaskForm):
    lost_item = SelectField('Item', choices=[], render_kw={'autofocus': True, 'id': 'lost_item_dropdown'})
    character = SelectField('Character', choices=[], render_kw={'id': 'character_dropdown'})

class SeedForm(FlaskForm):
    seed1 = SelectField('Seed 1', choices=[], render_kw={'autofocus': True, 'id': 'seed1_dropdown'})
    seed2 = SelectField('Seed 2', choices=[], render_kw={'id': 'seed2_dropdown'})
    seed3 = SelectField('Seed 3', choices=[], render_kw={'id': 'seed3_dropdown'})
    seed4 = SelectField('Seed 4', choices=[], render_kw={'id': 'seed4_dropdown'})
    seed5 = SelectField('Seed 5', choices=[], render_kw={'id': 'seed5_dropdown'})

    c_methods = [(0, ''), (1, 'Infuse with magic'), (2, 'Pour Airmid water'), (3, 'Prune'),
                 (4, 'Scatter Bonemeal'), (5, 'Use Caledonian soil'), (6, 'Spread pegasus blessings')]
    cultivation = SelectField('Cultivation', choices=c_methods, render_kw={'id': 'cultivation_dropdown'})

    clear_all = SubmitField('Clear all')
