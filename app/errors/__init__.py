"""Initialize the error-handling blueprint.

This subpackage sets up routing for error pages.

Modules:
    - handlers: Defines application error handlers.
"""

from flask import Blueprint


bp = Blueprint('errors', __name__)

from app.errors import handlers
