from flask import Blueprint, render_template


home = Blueprint('home', __name__, url_prefix='/')

@home.route('/', methods=['GET', 'POST'])
def index():
    """Show all stocks"""
    return render_template('index.html')