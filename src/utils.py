from flask import json
from src.database import Preferences

def load_languages():
    """load language data"""
    with open('./src/static/data/languages.json') as language_data:
        language_data = json.load(language_data)

    return {"languages":language_data['languages']}


def load_stocks():
    """load symbol data"""
    with open('./src/static/data/stocks_data.json') as symbol_data:
        stock_data = json.load(symbol_data)

    return {"stocks": stock_data['stocks']}


def load_resources():
    with open('./src/static/data/resources.json') as resources:
        resources = json.load(resources)

    return {"resources": resources['resources']}

def load_videos():
    with open('./src/static/data/videos.json') as videos:
        videos = json.load(videos)

    return {"videos": videos['video']}


def get_preferences(user):
    """
    Get user preferences
    input: user
    """
    try:
        preferences = Preferences.query.filter_by(user_id=user.id).first()
        print(preferences)
        return preferences
    except:
        message = "No preferences set"
        print(message)
        return message

