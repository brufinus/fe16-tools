from flask import render_template, redirect, request, jsonify, flash
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
    flash(choices)
    form.character1.choices = choices
    form.character2.choices = choices

    menu = []
    num_chars = 1

    # if form.validate_on_submit():
    cid1 = form.character1.data
    cid2 = form.character2.data
    if cid1 is None:
        num_chars = 0
    elif cid1 == cid2:
        db_char = db.session.get(Character, cid1)
        query = db_char.likes.select()
        menu = db.session.scalars(query).all()
    else:
        menu = db.session.query(Menu).join(liked_meals, Menu.id == liked_meals.c.dish_id) \
            .filter((liked_meals.c.diner_id == cid1) | (liked_meals.c.diner_id == cid2)) \
            .group_by(Menu.id) \
            .having(func.count(liked_meals.c.diner_id) == 2) \
            .all()
        num_chars = 2
    redirect('')

    return render_template('meal_finder.html', title='Meal Finder',
                           page_name='Dining Hall Meal Finder', form=form, menu=menu, num_chars=num_chars)

@app.route('/get_data', methods=['POST'])
def get_data():
    selected_option = int(request.json['selected_option'])
    data = get_choices(Character)

    return jsonify({'info': data[selected_option]})