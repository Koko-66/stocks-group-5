# https://www.youtube.com/watch?v=RLKW7ZMJOf4
from flask import session
from src.database import User
from src.tests import _auth as auth

def test_render_home(client, app):
    """Test renering home page"""
    response = client.get('/')
    with app.app_context():
        assert response.status_code == 200


def test_registration(client, app):
    """Test user registration"""
    response = auth.register(client)

    with app.app_context():
        assert response.status_code == 200
        assert User.query.count() == 1
        assert User.query.first().email == 'test@sample.com'


def test_login(client, app):
    """Test user login"""
    response = auth.login(client)

    # assert page redirecting after loging
    with app.app_context():
        assert response.status_code == 302
    # assert user is in session
    with client.session_transaction() as session:
        assert session['user_id'] == 1


def test_logout(client, app):
    """Test user logout"""
    
    response = client.get("auth/logout")
    with app.app_context():
        assert response.status_code == 302
    
    with client.session_transaction() as session:
        assert session == {}
        assert session == {}
