from flask import render_template, redirect, request, jsonify
from sqlalchemy import func

from app import app, db
from app.forms import CharacterForm, get_choices
from app.models import Character, Menu, liked_meals

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

@app.route('/meal-finder', methods=['GET', 'POST'])
def meal_finder():
    form = CharacterForm()
    choices = get_choices(Character)
    form.character1.choices = choices
    form.character2.choices = choices

    redirect('')

    return render_template('meal_finder.html', title='Meal Finder',
                           page_name='Dining Hall Meal Finder', form=form)

@app.route('/get_data', methods=['POST'])
def get_data():
    cid1 = int(request.json['selected_option1'])
    cid2 = int(request.json['selected_option2'])

    if cid1 == cid2:
        db_char = db.session.get(Character, cid1)
        query = db_char.likes.select()
        menu = db.session.scalars(query).all()
        num_chars = 1
    else:
        menu = db.session.query(Menu).join(liked_meals, Menu.id == liked_meals.c.dish_id) \
            .filter((liked_meals.c.diner_id == cid1) | (liked_meals.c.diner_id == cid2)) \
            .group_by(Menu.id) \
            .having(func.count(liked_meals.c.diner_id) == 2) \
            .all()
        num_chars = 2

    meals_data = [{'meal': meal.meal} for meal in menu]
    meals_count = len(menu)

    return jsonify({'meals': meals_data,
                    'meals_count': meals_count,
                    'num_chars': num_chars})