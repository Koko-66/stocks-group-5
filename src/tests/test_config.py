class Config(object):
    TESTING = False

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    TESTING = True
    SECRET_KEY = 'dev'