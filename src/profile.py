from flask import (Blueprint,
                   render_template,
                   redirect,
                   request)
from src.database import db, User, Preferences, Stock
from src.utils import load_languages, load_stocks, get_preferences
from src.auth import login_required

profile = Blueprint('profile', __name__, url_prefix='/profile')


@profile.route('/<username>', methods=['GET', 'POST'])
@login_required
def manage_profile(username):
    """Show all stocks"""

    message = ''
    preferred_language = ''
    languages = load_languages()
    stocks = load_stocks()

    # get current user from the database
    user = User.query.filter_by(username=username).first()
    user_id = user.id
    # get user preferences from the database
    preferences = Preferences.query.filter_by(user_id=user_id).first()
    preferred_stocks = preferences.stocks
    preferred_language = preferences.news_language
    
    return render_template('profile.html',
                           user=user,
                           username=username,
                           preferences=preferences,
                           languages=languages['languages'],
                           preferred_language = preferred_language,
                           message=message,
                           stocks=stocks['stocks'],
                           preferred_stocks=preferred_stocks
                           )


@profile.route('/<username>/update_stocks', methods=['POST', 'GET'])
@login_required
def update_stocks_preferences(username):
    """Update stock preferences"""
    # message = ""
    #  get current user from the database
    user = User.query.filter_by(username=username).first()
    # get user preferences from the database
    preferences = get_preferences(user)

    if request.method == 'POST':
        preferred_stock = request.form.get('stocks')
        print('request', preferred_stock)
        symbol = preferred_stock.split('-')[0]
        name = preferred_stock.split('-')[1]

        # check if stock already exits
        existing_stock = Stock.query.filter_by(symbol=symbol).first()

        if existing_stock is not None:
            
            preferred_stock = existing_stock
        else:
            preferred_stock = Stock(symbol=symbol,
                                    name=name)
            
        preferences.stocks.append(preferred_stock)

        db.session.add(preferences)
        db.session.commit()
    
    return redirect('/..')

@profile.route('/<username>/update_language', methods=['POST', 'GET'])
@login_required
def update_language_preferences(username):
    """Update user language preference"""
    # get current user from the database
    user = User.query.filter_by(username=username).first()
    # get user preferences from the database
    preferences = get_preferences(user)

    if request.method == 'POST':
        preferred_language = request.form.get('language')
        preferences.news_language = preferred_language

        db.session.add(preferences)
        db.session.commit()

    return redirect('/..')
