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
    languages = {"ar": "Arabic","de": "German", "en": "English", "es": "Spanish",
                 "fr": "French", "he": "Hebrew", "it": "Italian", "nl": "Dutch", 
                 "no": "Norwegian", "pt": "Portuguese", "ru": "Russian",
                 "se": "Swedish", "zh": "Chinese"}
    
    #handle
    if request.method == 'POST':
        selected_language = request.form.get('language', 'en')

    """Show news about stocks"""
    conn = http.client.HTTPConnection('api.mediastack.com')
    # Use keywords for web search as stock id related content.
    keywords = "google"

    # Define the parameters of the web search.
    params = urllib.parse.urlencode({
        'access_key': os.getenv('MEDIASTACK_API_KEY'),
        # 'categories': 'general',
        'sort': 'published_desc',
        'limit': 5,
        'languages': selected_language,
        'search': keywords,
        'keywords': keywords
    })
    conn.request('GET', '/v1/news?{}'.format(params))
    res = conn.getresponse()
    news_data = res.read()
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
                           languages=languages,
                           selected_language=selected_language)

