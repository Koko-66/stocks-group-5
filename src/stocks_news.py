"""Routes for the stocks page."""
import http.client
import json
# import matplotlib.pyplot as plt
import urllib.parse
import os
from flask import Blueprint, render_template, request

# import yfinance as yf
# import sqlite3


stocks_news = Blueprint('stocks_news', __name__, url_prefix='/stocks/news')

@stocks_news.route('/', methods=['GET', 'POST'])
def get_news():
    """Get news about stocks"""
    # Define the parameters of the web search.
    # List of available languages: https://mediastack.com/documentation
    # languages = {"ar": "Arabic","de": "German", "en": "English", "es": "Spanish",
    #              "fr": "French", "he": "Hebrew", "it": "Italian", "nl": "Dutch", 
    #              "no": "Norwegian", "pt": "Portuguese", "pl": "Polish", "ru": "Russian",
    #              "se": "Swedish", "tr": "Turkish", "th": "Thai", "zh": "Chinese"}

    with open('./src/static/data/languages.json') as language_data:
        language_data = json.load(language_data)
        
    with open('./src/static/data/stocks_data.json') as symbol_data:
        stock_data = json.load(symbol_data)
    
    #handle
    if request.method == 'POST':
        selected_language = request.form.get('language') #default language to be changed to prefereces language
        selected_symbol = request.form.get('stocks') #default symbols to be changed to prefereces symbols
    else:
        selected_language = 'multi'
        selected_symbol = ''
    conn = http.client.HTTPSConnection('api.marketaux.com')

    # Define the parameters of the web search.
    params = urllib.parse.urlencode({
        'api_token': os.environ.get('MARKETAUX_API_KEY'),
        'sort': 'published_desc',
        'language': selected_language,
        'symbols': selected_symbol,
    })
    conn.request('GET', '/v1/news/all?{}'.format(params))
    res = conn.getresponse()
    news_data = res.read()
    print(news_data)
    print(news_data.decode("utf-8"))
    # parse the response data as JSON
    news_data = json.loads(news_data)
    # Extract the title and URL of the article.
    try:
        articles = news_data['data']
    except KeyError:
        articles = []
    # Print the title and URL.

    conn.close()
    
    # add handling same articles from different sources - so that they do not repeat!
    
    
    return render_template('stocks_news.html', 
                           news_data=news_data, 
                           articles=articles,
                           languages=language_data['languages'],
                           stocks=stock_data['stocks'],
                           selected_language=selected_language,
                           selected_symbol=selected_symbol)

