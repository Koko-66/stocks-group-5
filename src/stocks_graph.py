"""Routes for the stocks graph page."""
import json
import pandas as pd
import yfinance as yf
from flask import Blueprint, request, render_template
from datetime import date, timedelta
# import sqlite3


stocks_graph = Blueprint('stocks_graph', __name__, url_prefix='/stocks_graph')


@stocks_graph.route('/', methods=['GET'])
def render():
    default = 'TSLA'
    if request.args.get('stock') == None:
        dates, prices=closing_price(default)
        stock=default
    else:
        args = request.args
        stock = args.get('stock')
        dates, prices=closing_price(stock)

    dates_json = json.dumps(dates)
    prices_json = json.dumps(prices)

    return render_template('stocks_graph.html',dates=dates_json, prices=prices_json, stock=stock)

def closing_price(stock):
    Start = date.today() - timedelta(365)
    Start.strftime('%Y-%m-%d')

    End = date.today() + timedelta(2)
    End.strftime('%Y-%m-%d')

    Asset = yf.download(stock, start=Start,
      end=End)['Adj Close']
    
    Asset = Asset.to_dict()
    temp_dates=list(Asset.keys())
    dates=[date_obj.strftime('%Y-%m-%d') for date_obj in temp_dates]
    prices=list(Asset.values())

    return dates, prices