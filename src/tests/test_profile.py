from src.tests import _auth as auth

from src.database import Stock

def test_profile_update_stocks_preferences(client, app):
    auth.login(client)
    response = client.post('profile/testuser/update_stocks', data={
        'stocks':'AAL-American Airlines Group Inc. Common Stock'})
    with app.app_context():
        assert response.status_code == 302
        assert Stock.query.first().symbol == 'AAL'