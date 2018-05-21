import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:1qaz2wsx@localhost/'
    
    if "DATABASE_URL" in os.environ:
        if os.environ['DATABASE_URL']:
            print('run os environment variable DATABASE_URL')
            print(os.environ['DATABASE_URL'])
            SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:1qaz2wsx@localhost/'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True