from flask import Blueprint, redirect, render_template, session


home = Blueprint('home', __name__, url_prefix='/')

@home.route('/', methods=['GET', 'POST'])
def index():
    """Show all stocks"""
    # redirect user to profile page is logged in (need a different checking method)
    try:
        if session['username']:
            return redirect(f"../profile/{session['username']}")
    except KeyError:
        return render_template('index.html')