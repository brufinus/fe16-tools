import os

import pytest

from app import create_app, db
from config import basedir


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": 'sqlite:///' + os.path.join(basedir, 'app.db'),
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    })

    yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture(scope='session')
def db_context(app):
    with app.app_context():
        yield db

def test_home_page(client):
    response = client.get('/index')
    assert b'<p>A collection of tools for helping with gameplay in Fire Emblem: Three Houses.</p>' in response.data
