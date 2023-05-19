"""Routes for the stocks page."""
import http.client
import json
import urllib.parse
import os
from flask import Blueprint, render_template, request, session
from src.database import db, User, Preferences
from src.utils import load_languages, load_stocks, get_preferences

# register the stocks_news blueprint
stocks_news = Blueprint('stocks_news', __name__, url_prefix='/profile')


# @stocks_news.route('/', methods=['GET', 'POST'])
# def get_news():
#     """Get news about stocks"""
#     # load data form json files
#     with open('./src/static/data/languages.json') as language_data:
#         language_data = json.load(language_data)

#     with open('./src/static/data/stocks_data.json') as symbol_data:
#         stock_data = json.load(symbol_data)

#     # handle post request
#     if request.method == 'POST':
#         selected_language = request.form.get('language')
#         selected_symbol = request.form.get('stocks')
#     else:
#         # if langugage set in the user preferences, then use it       
#         selected_language = 'en'
#         # if symbols set in the user preferences, then use it
#         selected_symbol = ''

#     # Create a connection for the HTTP request.
#     conn = http.client.HTTPSConnection('api.marketaux.com')

#     # Define the parameters of the web search.
#     params = urllib.parse.urlencode({
#         'api_token': os.environ.get('MARKETAUX_API_KEY'),
#         'sort': 'published_desc',
#         'language': selected_language,
#         'symbols': selected_symbol,
#     })

#     # Send the HTTP request and read the response
#     conn.request('GET', '/v1/news/all?{}'.format(params))
#     res = conn.getresponse()
#     news_data = res.read()

#     # parse the response data as JSON
#     news_data = json.loads(news_data)
#     message = {}
#     # Handle empty response error
#     try:
#         articles = news_data['data']
#     except KeyError:
#         articles = []

#     # Close the connection
#     conn.close()

#     return render_template('stocks_news.html', 
#                            news_data=news_data, 
#                            articles=articles,
#                            languages=language_data['languages'],
#                            stocks=stock_data['stocks'],
#                            selected_language=selected_language,
#                            selected_symbol=selected_symbol,
#                            message=message)

@stocks_news.route('/<username>/news', methods=['GET', 'POST'])
def get_news(username):
    """Get news about stocks"""
    # load data form json files
    language_data = load_languages()
    stock_data = load_stocks()
    
    user = User.query.filter_by(id=session["user_id"]).first()
    preferences = get_preferences(user)
    
    if request.method == "GET":
        if preferences.news_language:  
            selected_language = preferences.news_language
            # if symbols set in the user preferences, then use it
        else:
            selected_language = 'en'
        
        if preferences.stocks:
            selected_symbol = preferences.stocks[1]
    else:
    # if request.method == 'POST':
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