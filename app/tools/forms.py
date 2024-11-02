"""Define forms for the tools blueprint.

This module contains form classes for user input on each gameplay tool.

Classes:
    - CharacterForm: Single-character dropdown.
    - DualCharacterForm: Double-character dropdown.
    - ItemForm: Lost item and character dropdowns.
    - LectureForm: Lecture question search field.
    - SeedForm: Multiple seed dropdowns and cultivation method dropdown.
"""

from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CharacterForm(FlaskForm):
    """Form for a single-character dropdown.

    Attributes:
        character (SelectField): Dropdown for the character selection.
    """

    character = SelectField('Character', choices=[], render_kw={'autofocus': True, 'id': 'dropdown'})


class DualCharacterForm(FlaskForm):
    """Form for two character dropdowns.

    Attributes:
        character1 (SelectField): Dropdown for the first character selection.
        character2 (SelectField): Dropdown for the second character selection.
    """

    character1 = SelectField('Character 1', choices=[], render_kw={'autofocus': True, 'id': 'dropdown1'})
    character2 = SelectField('Character 2', choices=[], render_kw={'id': 'dropdown2'})


class ItemForm(FlaskForm):
    """Form for the item helper tool.

    Renders a lost item dropdown and a character dropdown for liked gifts.

    Attributes:
        lost_item (SelectField): Dropdown for the lost item selection.
        character (SelectField): Dropdown for the character selection.
    """

    lost_item = SelectField('Item', choices=[], render_kw={'autofocus': True, 'id': 'lost_item_dropdown'})
    character = SelectField('Character', choices=[], render_kw={'id': 'character_dropdown'})


class LectureForm(FlaskForm):
    """Form for the lecture assistant tool.

    Renders a search field for user inputted lecture questions.

    Attributes:
        question_query (StringField): Search field for the lecture question input.
    """

    question_query = StringField('Press Enter to clear.', validators=[DataRequired(), Length(max=25)],
                                 id='search-bar')


class SeedForm(FlaskForm):
    """Form for the seed simulator tool.

    Renders multiple dropdowns for greenhouse seed selections and the cultivation method.

    Attributes:
        seed1 (SelectField): Dropdown for the first seed selection.
        seed2 (SelectField): Dropdown for the second seed selection.
        seed3 (SelectField): Dropdown for the third seed selection.
        seed4 (SelectField): Dropdown for the fourth seed selection.
        seed5 (SelectField): Dropdown for the fifth seed selection.
        cultivation (SelectField): Dropdown for the cultivation method.
    """

    seed1 = SelectField('Seed 1', choices=[], render_kw={'autofocus': True, 'id': 'seed1_dropdown'})
    seed2 = SelectField('Seed 2', choices=[], render_kw={'id': 'seed2_dropdown'})
    seed3 = SelectField('Seed 3', choices=[], render_kw={'id': 'seed3_dropdown'})
    seed4 = SelectField('Seed 4', choices=[], render_kw={'id': 'seed4_dropdown'})
    seed5 = SelectField('Seed 5', choices=[], render_kw={'id': 'seed5_dropdown'})

    c_methods = [(0, ''), (1, 'Infuse with magic'), (2, 'Pour Airmid water'), (3, 'Prune'),
                 (4, 'Scatter Bonemeal'), (5, 'Use Caledonian soil'), (6, 'Spread pegasus blessings')]
    cultivation = SelectField('Cultivation', choices=c_methods, render_kw={'id': 'cultivation_dropdown'})

    clear_all = SubmitField('Clear all')
