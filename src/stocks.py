from flask import Blueprint, render_template, request, redirect, url_for, flash


stocks = Blueprint('stocks', __name__, url_prefix='/stocks')

@stocks.route('/', methods=['GET', 'POST'])
def index():
    """Show all stocks"""
    return render_template('index.html')