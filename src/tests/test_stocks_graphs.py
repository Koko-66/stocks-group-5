from src.tests import _auth as auth

def test_render_stocks(client, app):
    auth.login(client)
    response = client.get('/stocks_graph/')
    with app.app_context():
        assert response.status_code == 200

