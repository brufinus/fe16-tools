"""Define routes for the main blueprint

This module provides the view function for the main screen.

Functions:
    - index: Render the main application screen.
"""

from flask import redirect, render_template, request

from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    """Render the main screen.

    This view function renders a link to each tool on the main screen and redirects users to the short hostname.

    :return: The rendered template for the main screen.
    :rtype: str
    """

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
            'id': 'tools.lecture_assistant'
        }
    ]

    if request.host == 'fe16-tools-33427842621.us-central1.run.app':
        return redirect('https://fe16-tools.web.app', code=301)

    return render_template('index.html', title='Home', page_name='FE16 Tools', tools=tools)
