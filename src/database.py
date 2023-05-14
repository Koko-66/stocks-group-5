from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import unique
from sqlalchemy.orm import backref


db = SQLAlchemy()


class User(db.Model):
    #creating database/setting up parameters for columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    #columns to reflect datetime of registration and updates of user info
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    preferences = db.relationship('Preferences', backref="user")
    """ to create relationship with shares db if stored stocks=db.relationship('Shares', backref="user") can be inserted 
    and column user_id = db.Column(db.Integer, db.ForeignKey('user.id')) created in shares db"""
    #create string representation of our class
    def __repr__(self) -> str:
        return 'User>>> {self.username}'

stocks_preferences = db.Table('stocks_preferences',
    db.Column('stock_id', db.Integer, db.ForeignKey('stock.id'), primary_key=True),
    db.Column('preferences_id', db.Integer, db.ForeignKey('preferences.id'), primary_key=True)
)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
class Preferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    stocks = db.relationship('Stock', backref="notifications")
    alert_frequency = db.Column(db.String(10), nullable=False)
    news_preference = db.Column(db.String(50), nullable=False)
    news_language = db.Column(db.String(3), nullable=False)
