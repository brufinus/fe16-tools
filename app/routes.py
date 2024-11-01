from flask import render_template, redirect, request, jsonify
from app import app
from app.forms import LectureForm
from app.models import LectureQuestion


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
            'id': 'tools.seed_simulator'
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
