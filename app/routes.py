from math import floor
from flask import render_template, redirect, request, jsonify
from app import app, db
from app.forms import SeedForm, LectureForm
from app.models import Seed, LectureQuestion
from app.utility import get_choices, get_yield_ratios


@app.route('/')
@app.route('/index')
def index():
    tools = [
        {
            'name': 'Meal Finder',
            'description': 'Find shared liked meals between characters.',
            'id': 'tools.meal_finder'
        },
        {
            'name': 'Tea Helper',
            'description': 'Get favorite teas, liked topics, and correct responses.',
            'id': 'tools.tea_helper'
        },
        {
            'name': 'Item Helper',
            'description': 'Help return lost items and deliver liked gifts.',
            'id': 'tools.item_helper'
        },
        {
            'name': 'Seed Simulator',
            'description': 'Simulate Greenhouse seed combinations.',
            'id': 'seed_simulator'
        },
        {
            'name': 'Lecture Assistant',
            'description': 'Correctly answer the monthly lecture question.',
            'id': 'lecture_assistant'
        }
    ]

    if request.host == 'fe16-tools-33427842621.us-central1.run.app':
        return redirect('https://fe16-tools.web.app', code=301)

    return render_template('index.html', title='Home', page_name='FE16 Tools', tools=tools)

@app.route('/seed-simulator', methods=['GET', 'POST'])
def seed_simulator():
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

    return render_template('seed_simulator.html', title='Seed Sim',
                           page_name='Seed Simulator', form=form)

@app.route('/get_seed_data', methods=['POST'])
def get_seed_data():
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

@app.route('/lecture-assistant', methods=['GET'])
def lecture_assistant():
    form = LectureForm()

    return render_template('lecture_assistant.html', title='Lecture Assist',
                           page_name='Lecture Assistant', form=form)

@app.route('/get_lecture_data', methods=['POST'])
def get_lecture_data():
    query = request.json.get('q', '')
    if query:
        results = LectureQuestion.query.filter(LectureQuestion.question.ilike(f'%{query}%')).all()
        data = [{'id': q.id, 'question': q.question, 'answer': q.answer} for q in results]
        return jsonify({'data': data})
    return jsonify({'data': []})
