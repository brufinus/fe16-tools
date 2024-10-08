from flask import render_template, redirect, request, jsonify
from sqlalchemy import func
from app import app, db
from app.forms import CharacterForm, DualCharacterForm, get_choices, ItemForm
from app.models import Character, Menu, liked_meals, TeaTopic, LostItem, Gift, liked_gifts
import sqlalchemy as sa


@app.route('/')
@app.route('/index')
def index():
    tools = [
        {
            'name': 'Meal Finder',
            'description': 'Find shared liked meals between characters.',
            'id': 'meal_finder'
        },
        {
            'name': 'Tea Helper',
            'description': 'Get favorite teas, liked topics, and correct responses.',
            'id': 'tea_helper'
        },
        {
            'name': 'Item Helper',
            'description': 'Help return lost items and deliver liked gifts.',
            'id': 'item_helper'
        }
    ]

    if request.host == 'fe16-tools-33427842621.us-central1.run.app':
        return redirect('https://fe16-tools.web.app', code=301)

    return render_template('index.html', title='Home', page_name='FE16 Tools', tools=tools)

@app.route('/meal-finder', methods=['GET', 'POST'])
def meal_finder():
    form = DualCharacterForm()
    choices = get_choices(Character)
    form.character1.choices = choices
    form.character2.choices = choices

    redirect('')

    return render_template('meal_finder.html', title='Meal Finder',
                           page_name='Dining Hall Meal Finder', form=form)

@app.route('/get_meal_data', methods=['POST'])
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

@app.route('/tea-helper', methods=['GET', 'POST'])
def tea_helper():
    form = CharacterForm()
    choices = get_choices(Character)
    form.character.choices = choices

    redirect('')

    return render_template('tea_helper.html', title='Tea Helper',
                           page_name='Tea Party Helper', form=form)

@app.route('/get_tea_data', methods=['POST'])
def get_tea_data():
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

@app.route('/item-helper', methods=['GET', 'POST'])
def item_helper():
    form = ItemForm()
    lost_item_choices = get_choices(LostItem)
    character_choices = get_choices(Character)
    form.lost_item.choices = lost_item_choices
    form.character.choices = character_choices

    redirect('')

    return render_template('item_helper.html', title='Item Helper', page_name='Item Helper', form=form)

@app.route('/get_item_data', methods=['POST'])
def get_item_data():
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
