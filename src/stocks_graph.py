"""Routes for the stocks graph page."""
import json
from datetime import date, timedelta
import yfinance as yf
from flask import Blueprint, request, render_template,session
from src.auth import login_required
from src.database import User
from src.utils import get_preferences


stocks_graph = Blueprint('stocks_graph', __name__, url_prefix='/stocks_graph')


@stocks_graph.route('/', methods=['GET'])
@login_required
def render():
    if session:
        user = User.query.filter_by(id=session["user_id"]).first()
        preferences = get_preferences(user)
    
        default = preferences.stocks[0].symbol
        preferred_stocks = preferences.stocks
        if request.args.get('stock') == None:
            dates, prices=closing_price(default)
            stock=default
        else:
            args = request.args
            stock = args.get('stock')
            dates, prices=closing_price(stock)

        dates_json = json.dumps(dates)
        prices_json = json.dumps(prices)
        
        last_price = float(json.dumps(prices[-1]))
        prev_last_price = float(json.dumps(prices[-2]))
        
        price_change = last_price - prev_last_price
        
        perc_change = price_change / prev_last_price * 100

        return render_template('stocks_graph.html',
                            preferences=preferences,
                            preferred_stocks=preferred_stocks,
                            dates=dates_json,
                            last_price=round(last_price),
                            prev_last_price=prev_last_price,
                            price_change=round(price_change, 2),
                            percent=round(perc_change, 2),
                            prices=prices_json,
                            stock=stock,
                            username=user.username)

    else:
        return render_template('index.html')

 
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
