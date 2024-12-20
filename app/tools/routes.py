"""Define routes for the tools blueprint.

This module provides view functions for each gameplay tool.

Functions:
    - meal_finder: Render the meal finder tool.
    - get_meal_data: Get response liked meal data in json format.
    - tea_helper: Render the tea helper tool.
    - get_tea_data: Get response tea party data in json format.
    - item_helper: Render the item helper tool.
    - get_item_data: Get response lost item and gift data in json format.
    - seed_simulator: Render the seed simulator tool.
    - get_seed_data: Get response greenhouse seed data in json format.
    - lecture_assistant: Render the lecture assistant tool.
    - get_lecture_data: Get response monthly lecture data in json format.
"""

from math import floor

import sqlalchemy as sa
from app import db
from flask import jsonify, redirect, render_template, request
from sqlalchemy import func

from app.models import liked_meals, liked_gifts, Character, Gift, LectureQuestion, LostItem, Menu, Seed, TeaTopic
from app.tools import bp
from app.tools.forms import CharacterForm, DualCharacterForm, ItemForm, LectureForm, SeedForm
from app.tools.utility import get_choices, get_yield_ratios


@bp.route('/meal-finder', methods=['GET'])
def meal_finder():
    """Render the meal finder tool.

    This view function grabs the options for the character form and renders the meal finder template.

    :return: The rendered template for the meal finder tool.
    :rtype: str
    """

    form = DualCharacterForm()
    choices = get_choices(Character, True)
    form.character1.choices = choices
    form.character2.choices = choices

    return render_template('tools/meal_finder.html', title='Meal Finder',
                           page_name='Dining Hall Meal Finder', form=form)

@bp.route('/get_meal_data', methods=['POST'])
def get_meal_data():
    """Get liked meal data.

    This view function returns data on characters' shared liked meals in json format.

    :return: The liked meal data in json format.
    :rtype: Response
    """

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

@bp.route('/tea-helper', methods=['GET'])
def tea_helper():
    """Render the tea helper tool.

    This view function grabs the options for the character form and renders the tea helper template.

    :return: The rendered template for the tea helper tool.
    :rtype: str
    """

    form = CharacterForm()
    choices = get_choices(Character, True)
    form.character.choices = choices

    return render_template('tools/tea_helper.html', title='Tea Helper',
                           page_name='Tea Party Helper', form=form)

@bp.route('/get_tea_data', methods=['POST'])
def get_tea_data():
    """Get tea party data.

    This view function returns data on a character's liked teas, topics, and final
    comments and answers during a tea party. The data is returned in json format.

    :return: The tea party data in json format.
    :rtype: Response
    """

    cid = int(request.json['selected_option'])
    char = db.session.get(Character, cid)

    query = char.likes_tea.select()
    tea = db.session.scalars(query).all()
    tea_data = [{'tea': t.name} for t in tea]
    tea_count = len(tea)

    query = char.likes_tea_topic.select().order_by(TeaTopic.data)
    topics = db.session.scalars(query).all()
    topic_data = [{'topic': t.data} for t in topics]

    final_topics = sorted(char.final_tea_comment, key=lambda final_topic: final_topic.comment)
    comment_data = []
    answer_data = []
    for topic in final_topics:
        comment_data.append({'comment': topic.comment})
        answer_data.append({'answer': topic.response})

    return jsonify({'tea': tea_data,
                    'tea_count': tea_count,
                    'topics': topic_data,
                    'comments': comment_data,
                    'answers': answer_data})

@bp.route('/item-helper', methods=['GET'])
def item_helper():
    """Render the item helper tool.

    This view function grabs the options for the lost item and character forms and renders the item helper template.

    :return: The rendered template for the item helper tool.
    :rtype: str
    """

    form = ItemForm()
    lost_item_choices = get_choices(LostItem, True)
    character_choices = get_choices(Character, True)
    form.lost_item.choices = lost_item_choices
    form.character.choices = character_choices

    return render_template('tools/item_helper.html', title='Item Helper', page_name='Item Helper',
                           form=form)

@bp.route('/get_item_data', methods=['POST'])
def get_item_data():
    """Get lost item and liked gift data.

    This view function returns data on owners of items lost around the monastery
    as well as gifts that characters like. The data is returned in json format.

    :return: The lost item and liked gift data in json format.
    :rtype: Response
    """

    lid = int(request.json['lost_item_selected_option'])
    lost_item = db.session.get(LostItem, lid)
    character = lost_item.owner.name
    character_data = [{'character': character}]

    cid = int(request.json['character_selected_option'])
    query = sa.select(Gift).join(liked_gifts).where(liked_gifts.c.character_id == cid)
    gifts = db.session.scalars(query).all()
    gift_data = [{'name': gift.name} for gift in gifts]

    return jsonify({'character': character_data,
                    'gifts': gift_data})

@bp.route('/seed-simulator', methods=['GET', 'POST'])
def seed_simulator():
    """Render the seed simulator tool.

    This view function grabs the options for the seed forms and renders the seed simulator template.

    :return: The rendered template for the seed simulator tool.
    :rtype: str
    """

    form = SeedForm()
    seed_choices = [(-1, '')]
    seed_choices.extend(get_choices(Seed, False))
    seed_choices = [(sid, name.removesuffix(" Seeds")) for sid, name in seed_choices]
    form.seed1.choices = seed_choices
    form.seed2.choices = seed_choices
    form.seed3.choices = seed_choices
    form.seed4.choices = seed_choices
    form.seed5.choices = seed_choices

    if form.validate_on_submit():
        return redirect('')

    return render_template('tools/seed_simulator.html', title='Seed Sim',
                           page_name='Seed Simulator', form=form)

@bp.route('/get_seed_data', methods=['POST'])
def get_seed_data():
    """Get greenhouse seed data.

    This view function returns data on simulated greenhouse seed selections and returns it in json format.
    Hidden score calculation is performed here.

    :return: The selection score, yield, ratio, and stat-booster coefficient in json format.
    :rtype: Response
    """

    sids = [int(request.json[f'seed{i}_selected_option']) for i in range(1, 6)]
    unique_seeds = db.session.query(Seed).filter(Seed.id.in_(sids)).all()
    seed_map = {seed.id: seed for seed in unique_seeds}
    seeds = [seed_map[sid] for sid in sids if sid != -1]
    cultivation = int(request.json['cultivation_selected_option'])

    rank, grade = 0, 0
    for seed in seeds:
        rank += seed.rank
        grade += seed.grade

    if not seeds:
        score = 0
    else:
        x = (12 - (rank % 12)) * 5
        y = floor((grade / 5) * 4)
        z = (cultivation + 4) * 2
        score = x + y + z

    yld, ratio, coefficient = get_yield_ratios(score)

    return jsonify({'score': str(score),
                    'yield': str(yld),
                    'ratio': ratio,
                    'coefficient': str(coefficient)})

@bp.route('/lecture-assistant', methods=['GET'])
def lecture_assistant():
    """Render the lecture assistant tool.

    This view function renders the lecture assistant template.

    :return: The rendered template for the lecture assistant tool.
    :rtype: str
    """

    form = LectureForm()

    return render_template('tools/lecture_assistant.html', title='Lecture Assist',
                           page_name='Lecture Assistant', form=form)

@bp.route('/get_lecture_data', methods=['POST'])
def get_lecture_data():
    """Get monthly lecture data.

    This view function returns data on the monthly lecture question and returns it in json format.

    :return: The lecture question and answer in json format.
    :rtype: Response
    """

    query = request.json.get('q', '')
    if query:
        results = LectureQuestion.query.filter(LectureQuestion.question.ilike(f'%{query}%')).all()
        data = [{'id': q.id, 'question': q.question, 'answer': q.answer} for q in results]
        return jsonify({'data': data})
    return jsonify({'data': []})
