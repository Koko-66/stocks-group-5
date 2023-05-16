"""Routes for the stocks graph page."""
import io
import pandas as pd
import yfinance as yf
import matplotlib 
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Blueprint, request, render_template, send_from_directory
from matplotlib.figure import Figure
from datetime import date, timedelta
# import sqlite3


stocks_graph = Blueprint('stocks_graph', __name__, url_prefix='/stocks_graph',static_folder='static')

@stocks_graph.route('/', methods=['GET'])
def render():
    default = 'TSLA'
    if request.args.get('stock') == None:
        plot_png(default)
    else:
        args = request.args
        option = args.get('stock')
        print(option)
        plot_png(option)

    return render_template('stocks_graph.html')

# @stocks_graph.route('/plot')
def plot_png(stock):

    stock_cp = closing_price(stock)
    color = {"TSLA": "blue",
    "AMZN": "red",
    "GOOG": "green"}
    stock_fig = plot_price(stock_cp, color[stock], f'{stock} Performance')

    return send_from_directory(stocks_graph.static_folder,'img.png', mimetype='image/gif')

def closing_price(ticker):
    Start = date.today() - timedelta(365)
    Start.strftime('%Y-%m-%d')

    End = date.today() + timedelta(2)
    End.strftime('%Y-%m-%d')

    Asset = pd.DataFrame(yf.download(ticker, start=Start,
      end=End)['Adj Close'])     
    return Asset

def plot_price(ticker, color, head):
    img='src/static/img.png'
    plt.plot(ticker, color=color, linewidth=2)
    plt.title(head)
    plt.ylabel('Price ($)')
    plt.xlabel('Date')
    plt.savefig(img)
    plt.clf()
