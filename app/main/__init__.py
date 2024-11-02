"""Initialize the main blueprint.

This subpackage sets up routes related to the main application function.

Modules:
    - routes: Defines the main screen mapping.
"""

from flask import Blueprint


bp = Blueprint('main', __name__)

from app.main import routes
