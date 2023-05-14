from flask import Blueprint, render_template


# home = Blueprint('profile', __name__, url_prefix='/profile/<username>')
profile = Blueprint('profile', __name__, url_prefix='/profile')

@profile.route('/', methods=['GET', 'POST'])
def manage_profile():
    """Show all stocks"""
    return render_template('profile.html')