from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    #creating database/setting up parameters for columns
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.String(80), unjique=True, nullable=False)
    email = db.column(db.String(120), unjique=True, nullable=False)
    username = db.column(db.String(120), unjique=True, nullable=False)
    password = db.column(db.Text(), nullable=False)
    #columns to reflect datetime of registration and updates of user info
    created_at = db.column(db.DateTime, default=datetime.now())
    updated_at = db.column(db.DateTime, onupdate=datetime.now())
    bookmarks=db.relationship('Bookmark', backref="user")

    #create string representation of our class
    def __repr__(self) -> str:
        return 'User>>> {self.username}'

class Bookmark(db.Model):
    id = db.column(db.Integer, primary_key=True)
    body = db.column(db.Text(), nullable=True)
    url = db.column(db.Text(), nullable=False)
    short_url = db.column(db.Str(3), nullable=True)
    visits = db.column(db.Integer, default=0)
    user_id = db.column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.column(db.DateTime, default=datetime.now())
    updated_at = db.column(db.DateTime, onupdate=datetime.now())
