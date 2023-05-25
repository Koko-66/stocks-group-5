"""Routes for the stocks page."""
import http.client
import json
import urllib.parse
import os
from flask import Blueprint, render_template, request, session
from src.auth import login_required
from src.database import User
from src.utils import load_languages, load_stocks, get_preferences

# register the stocks_news blueprint
stocks_news = Blueprint('stocks_news', __name__, url_prefix='/profile')


@stocks_news.route('/<username>/news', methods=['GET', 'POST'])
@login_required
def get_news(username, stock=None):
    """Get news about stocks"""

    # load data form json files
    language_data = load_languages()
    stock_data = load_stocks()
    
    stock = request.args.get('stock')

    user = User.query.filter_by(id=session["user_id"]).first()
    preferences = get_preferences(user)

    # Handle get request
    if request.method == "GET":
        selected_language = preferences.news_language

        # Check is stock passed in request, if not check prefernces and select first
        # if not make no selection, first from the list
        if stock is None:
            if preferences.stocks:
                selected_symbol = preferences.stocks[0].symbol
            else:
                selected_symbol = stock_data['stocks'][1]
        # if accessed from the profile page for specific stock
        # take stock from request
        else:
            selected_symbol = request.args.get('stock')

    # Handle post request - user selection
    else:
        selected_language = request.form.get('language')
        selected_symbol = request.form.get('stocks')

    # Create a connection for the HTTP request.
    conn = http.client.HTTPSConnection('api.marketaux.com')

    # Define the parameters of the web search.
    params = urllib.parse.urlencode({
        'api_token': os.environ.get('MARKETAUX_API_KEY'),
        'sort': 'published_desc',
        'language': selected_language,
        'symbols': selected_symbol,
    })

    # Send the HTTP request and read the response
    conn.request('GET', '/v1/news/all?{}'.format(params))
    res = conn.getresponse()
    news_data = res.read()

    # parse the response data as JSON
    news_data = json.loads(news_data)
    # Handle empty response error
    try:
        articles = news_data['data']
    except KeyError:
        articles = []

    # Close the connection
    conn.close()

    return render_template('stocks_news.html',
                           stock = stock,
                           articles=articles,
                           languages=language_data['languages'],
                           stocks=stock_data['stocks'],
                           username=username,
                           preferences=preferences,
                           selected_language=selected_language,
                           selected_symbol=selected_symbol,
                        )