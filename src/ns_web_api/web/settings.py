# coding: utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:1qaz2wsx@localhost/'

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
