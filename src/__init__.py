from flask import Flask
import os
from src.auth import auth
from src.database import db


def create_app(test_config=None):
    """Create main app entry point"""
    app = Flask(__name__,
                instance_relative_config=True #specifies that the config files are relative to the instance folder
        ) 

    # load the instance config, if it exists, when not testing
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI")
            )
    # if test_config is not None, then the app is in test mode
    else:
        app.config.from_mapping(test_config)


    #initialising extensions
    db.app=app
    db.init_app(app)


    #registering blueprints
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)


    blueprints = ['stocks', 'home']
    for bp in blueprints:
        app.register_blueprint(__import__(f'src.{bp}', fromlist=[bp]).__getattribute__(bp))

    return app
