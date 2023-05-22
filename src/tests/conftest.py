import pytest
from src.tests.test_config import TestingConfig
from src import create_app, db

@pytest.fixture()
def app():
    test_config = TestingConfig()
    app = create_app(test_config)

    with app.app_context():
        db.create_all()

    yield app
    

@pytest.fixture()
def client(app):
    return app.test_client()