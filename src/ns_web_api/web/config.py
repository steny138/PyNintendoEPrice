class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:1qaz2wsx@localhost/'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:1qaz2wsx@localhost/'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True