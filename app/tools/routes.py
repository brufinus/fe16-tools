from app import db
from flask import jsonify, render_template, request
from sqlalchemy import func

from app.models import Character, Menu, liked_meals
from app.tools.forms import DualCharacterForm
from app.tools import bp
from app.utility import get_choices


@bp.route('/meal-finder', methods=['GET'])
def meal_finder():
    form = DualCharacterForm()
    choices = get_choices(Character, True)
    form.character1.choices = choices
    form.character2.choices = choices

    return render_template('tools/meal_finder.html', title='Meal Finder',
                           page_name='Dining Hall Meal Finder', form=form)

@bp.route('/get_meal_data', methods=['POST'])
def get_meal_data():
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
