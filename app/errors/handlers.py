"""Define routes for error-handling.

This module provides error-handling view functions.

Functions:
    - not_found_error: Render the error screens.
"""

from flask import render_template
from app import db
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    """Render the 404 error screen.

    :param error: The error passed to the handler.
    :type error: Any
    :return: The rendered template for the error screen and the error code.
    :rtype: tuple[str, int]
    """

    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def not_found_error(error):
    """Render the 500 error screen and roll back the database session.

    :param error: The error passed to the handler.
    :type error: Any
    :return: The rendered template for the error screen and the error code.
    :rtype: tuple[str, int]
    """

    db.session.rollback()
    return render_template('errors/500.html'), 500
