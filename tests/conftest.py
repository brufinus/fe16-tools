import pytest
from app import app, db

@pytest.fixture()
def tools_app():
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        yield app

@pytest.fixture()
def client(tools_app):
    with tools_app.test_client() as client:
        yield client

@pytest.fixture()
def runner(tools_app):
    return app.test_cli_runner()

@pytest.fixture()
def db_context(tools_app):
    with tools_app.app_context():
        yield db

def test_home_page(client):
    response = client.get('/index')
    assert b'<p>A collection of tools for helping with gameplay in Fire Emblem: Three Houses.</p>' in response.data