class Config(object):
    TESTING = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"