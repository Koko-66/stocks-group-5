# https://www.youtube.com/watch?v=RLKW7ZMJOf4
from flask import session
from src.database import User

def test_render_home(client, app):
    """Test renering home page"""
    response = client.get('/')
    with app.app_context():
        assert response.status_code == 200


def test_registration(client, app):
    """Test user registration"""
    response = client.post('auth/register', data={
        'username':'testuser',
        'email':'test@sample.com',
        'password':'somepassword'})

    with app.app_context():
        assert response.status_code == 200
        assert User.query.count() == 1
        assert User.query.first().email == 'test@sample.com'


def test_login(client, app):
    """Test user login"""
    response = client.post('auth/login', data={
        'username':'testuser',
        'email':'test@sample.com',
        'password':'somepassword'})

    # assert page redirecting after loging
    with app.app_context():
        assert response.status_code == 302
    # assert user is in session
    with client.session_transaction() as session:
        assert session['user_id'] == 1


def test_logout(client, app):
    """Test user logut"""
    
    response = client.get("auth/logout")
    with app.app_context():
        assert response.status_code == 302
    
    with client.session_transaction() as session:
        assert session['user_id'] not in session
