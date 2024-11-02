"""Initialize the Flask application and register blueprints for modules.

Modules:
    - models: Contains database models.

Subpackages:
    - errors: Blueprint containing error-handling routes.
    - main: Blueprint containing main application functionality.
    - tools: Blueprint containing logic and functionality for gameplay tools.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    """Create and configure the Flask application.

    Utilizes an application factory function to register blueprints and pass an application instance on runtime.

    :param config_class: The configuration object for the instance.
    :type config_class: Config
    :return: The Flask application instance.
    :rtype: Flask
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.tools import bp as tools
    app.register_blueprint(tools, url_prefix='/tools')

    from app.main import bp as main
    app.register_blueprint(main)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/tools.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d')
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Tools startup')

    return app


from app import models
