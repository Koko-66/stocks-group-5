from src.tests import _auth as auth
from src.database import Stock
from src.database import Preferences
import pytest


def test_profile_update_stocks_preferences(client, app):
    response = client.post('profile/testuser/update_stocks', data={
        'stocks':'AAL-American Airlines Group Inc. Common Stock'})
    with app.app_context():
        assert response.status_code == 302
        with pytest.raises(AttributeError):
            assert Stock.query.second().symbol == 'AAL'

def test_update_language_preferences(client,app):
    response = client.post('profile/testuser/update_language', data={
        'language':'fr'})
    with app.app_context():
        assert response.status_code == 302
        with pytest.raises(AttributeError):
            assert Preferences.query.second().news_language == 'fr'

def test_render_stocks(client, app):
    response = client.get('/stocks_graph/')
    with app.app_context():
        assert response.status_code == 302


def test_get_news(client, app):
    response = client.get('profile/testuser/news')
    with app.app_context():
        assert response.status_code == 302


def test_get_news_post(client, app):
    response = client.post('profile/testuser/news', data={
        'stocks':'AAL',
        'language':'fr'
    })
    with app.app_context():
        assert response.status_code == 302