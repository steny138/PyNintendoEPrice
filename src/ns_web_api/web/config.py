import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:1qaz2wsx@localhost/'

class ProductionConfig(Config):
    if "DATABASE_URL" in os.environ:
        if os.environ['DATABASE_URL']:
            SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:1qaz2wsx@localhost/'
    DEBUG = True

class TestingConfig(Config):
    TESTING = True