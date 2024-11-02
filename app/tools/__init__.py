"""Initialize the tools blueprint.

This subpackage sets up forms, routes, and utility modules related to gameplay tools within the application.

Modules:
    - forms: Defines rendered forms for each tool.
    - routes: Defines mappings to view functions for each tool.
    - utility: Contains helper functions for tool views.
"""

from flask import Blueprint


bp = Blueprint('tools', __name__)

from app.tools import forms, routes
