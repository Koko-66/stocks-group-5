from src.tests import _auth as auth

def test_get_news(client, app):
    auth.login(client)
    response = client.get('profile/testuser/news')
    with app.app_context():
        assert response.status_code == 200


def test_get_news_post(client, app):
    auth.login(client)    
    response = client.post('profile/testuser/news', data={
        'stocks':'AAL',
        'language':'fr'
    })
    with app.app_context():
        assert response.status_code == 200