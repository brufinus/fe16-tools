from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import CharacterForm, InsertForm, get_choices
from app.models import Character, Menu, liked_meals
import sqlalchemy as sa
import yaml

@app.route('/')
@app.route('/index')
def index():
    tools = [
        {
            'name': 'Meal Finder',
            'description': 'Find shared liked meals between two characters.'
        }
    ]
    return render_template('index.html', title='Home', page_name='FE16 Tools', tools=tools)

@app.route('/meal-finder', methods=['GET'])
def meal_finder():
    form = CharacterForm()
    choices = get_choices(Character)
    form.character1.choices = choices
    form.character2.choices = choices
    return render_template('meal_finder.html', title='Meal Finder',
                           page_name='Dining Hall Meal Finder', form=form)

# TODO: Delete me - for DB insertion only
# @app.route('/insert', methods=['GET', 'POST'])
# def insert():
#     form = InsertForm()
#     if form.validate_on_submit():
#         with open('liked_meals.yml') as stream:
#             try:
#                 liked_meals_dict = yaml.safe_load(stream)
#                 for meal_name in liked_meals_dict:
#                     menu = Menu(meal=meal_name)
#                     db.session.add(menu)
#                     mid = db.session.scalar(sa.select(Menu.id).where(Menu.meal == menu.meal))
#                     for character_name in liked_meals_dict[meal_name]:
#                         character = Character(name=character_name)
#                         cid = db.session.scalar(sa.select(Character.id).where(Character.name == character.name))
#                         if cid is None:
#                             db.session.add(character)
#                             cid = db.session.scalar(sa.select(Character.id).where(Character.name == character.name))
#                         statement = liked_meals.insert().values(diner_id=cid, dish_id=mid)
#                         db.session.execute(statement)
#                 db.session.commit()
#             except yaml.YAMLError as exc:
#                 print(exc)
#
#         flash('Character-Meal link inserted.')
#         return redirect(url_for('index'))
#     return render_template('insert.html', title='Insert', form=form)