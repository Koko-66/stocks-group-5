"""Routes for the stocks page."""
import http.client
import json
# import matplotlib.pyplot as plt
import urllib.parse
import os
from flask import Blueprint, render_template
import yfinance as yf
# import sqlite3


stocks = Blueprint('stocks', __name__, url_prefix='/stocks')

@stocks.route('/', methods=['GET'])
def connect_to_api():
    """Show all stocks"""
    conn = http.client.HTTPConnection('api.mediastack.com')
    # Use keywords for web search as stock id related content.
    keywords = "google"
    # Define the parameters of the web search.
    params = urllib.parse.urlencode({
        'access_key': os.getenv('MEDIASTACK_API_KEY'),
        'categories': 'general',
        'sort': 'published_desc',
        'limit': 5,
        'language': "en",
        'search': keywords,
        'keywords': keywords
    })
    conn.request('GET', '/v1/news?{}'.format(params))
    res = conn.getresponse()
    news_data = res.read()
    # parse the response data as JSON
    news_data = json.loads(news_data)
    # Extract the title and URL of the article.

    articles = news_data['data']
    # Print the title and URL.

    conn.close()
    
    
    return render_template('stocks.html', news_data=news_data, articles=articles)

