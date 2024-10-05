from flask import render_template, url_for
from app import app

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

@app.route('/meal-finder')
def meal_finder():
    return render_template('meal_finder.html', title='Meal Finder', page_name='Dining Hall Meal Finder')