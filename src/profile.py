import http.client
import json
import urllib.parse
import os

from flask import (Blueprint,
                   json,
                   render_template,
                   session,
                   request)
from src.database import db, User, Preferences

# home = Blueprint('profile', __name__, url_prefix='/profile/<username>')
profile = Blueprint('profile', __name__, url_prefix='/profile')


@profile.route('/<username>', methods=['GET', 'POST'])
def manage_profile(username):
    """Show all stocks"""
    message = ''
    preferred_language = ''
    preferred_stocks = []
    # get current user from the database
    user = User.query.filter_by(username=username).first()
    # get user preferences from the database
    preferences = Preferences.query.filter_by(user_id=user.id).first()
    # load language data
    with open('./src/static/data/languages.json') as language_data:
        language_data = json.load(language_data)
    # load symbol data
    with open('./src/static/data/stocks_data.json') as symbol_data:
        stock_data = json.load(symbol_data)
    
    if preferences:
        language_code = preferences.news_language
        preferred_language = language_data['languages'][language_code]
    else:
        message = 'No preferences yet'

    if request.method == 'POST':
        preferred_stock = request.form.get('symbol')
        preferred_language = request.form.get('language')
        if preferred_stock:
            preferred_stock = Preferences

    return render_template('profile.html',
                           user=user,
                           preferences=preferences,
                           languages=language_data['languages'],
                           preferred_language = preferred_language,
                           message=message,
                           stocks=stock_data['stocks']
                           )


@profile.route('/<username>/news', methods=['GET', 'POST'])
def get_news(username):
    """Get news about stocks"""
    # load data form json files
    with open('./src/static/data/languages.json') as language_data:
        language_data = json.load(language_data)

    with open('./src/static/data/stocks_data.json') as symbol_data:
        stock_data = json.load(symbol_data)
    
    user = User.query.filter_by(id=session["user_id"]).first()
    preferences = Preferences.query.filter_by(user_id=user.id).first()
                                
    # handle post request
    if request.method == 'POST':
        selected_language = request.form.get('language')
        selected_symbol = request.form.get('stocks')
        
    
        preferences = Preferences(user_id=user.id,
                                  news_language=selected_language)
        db.session.add(preferences)
        db.session.commit()
    
    # get request
    else:
        # if langugage set in the user preferences, then use it       
        selected_language = 'en'
        # if symbols set in the user preferences, then use it
        selected_symbol = ''

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
    message = {}
    # Handle empty response error
    try:
        articles = news_data['data']
    except KeyError:
        articles = []

    # Close the connection
    conn.close()

    return render_template('stocks_news.html', 
                           news_data=news_data, 
                           articles=articles,
                           languages=language_data['languages'],
                           stocks=stock_data['stocks'],
                           username=username,
                           preferences=preferences,
                           selected_language=selected_language,
                           selected_symbol=selected_symbol,
                           message=message)