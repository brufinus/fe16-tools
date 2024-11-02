"""Configuration settings for the Flask application.

Classes:
    - Config: Base configuration class.
"""

import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration class with default settings."""

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')