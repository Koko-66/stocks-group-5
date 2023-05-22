from flask import Flask, render_template, request, redirect, session, url_for
import os
from src.auth import auth
from src.database import db
from flask_session import Session
from src.auth import login_required



def create_app(test_config=None):
    """Create main app entry point"""
    app = Flask(__name__,
                instance_relative_config=True #specifies that the config files are relative to the instance folder
        ) 

    # load the instance config, if it exists, when not testing
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SESSION_TYPE='filesystem',
            SESSION_PERMANENT=True,
            SESSION_USE_SIGNER=True
        )
    # if test_config is not None, then the app is in test mode
    else:
        app.config.from_object(test_config)


    #initialising extensions
    db.app=app
    db.init_app(app)

    Session(app)


    #registering blueprints

    blueprints = ['auth', 'home', 'stocks_news', 'stocks_graph', 'profile', 'notifications']
    
    for bp in blueprints:
        app.register_blueprint(__import__(f'src.{bp}', fromlist=[bp]).__getattribute__(bp))

    return app
