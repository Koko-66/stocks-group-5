# Routes for the stocks page
import json
from flask import Blueprint, render_template, Flask, jsonify,  request
import finnhub


finnhub_client = finnhub.Client(api_key="chavn39r01qkns31agq0chavn39r01qkns31agqg")
stock_prefs = Blueprint('stock_prefs', __name__, url_prefix='/stock_prefs')


@stock_prefs.route('/', methods=['GET', 'POST'])
def stock_choice():
    with open(
        'static/data/stocks_data.json') as symbol_data:
        stock_list = json.load(symbol_data)
        stocks = stock_list['stocks']
        return render_template('stock_prefs.html', stocks=stocks)