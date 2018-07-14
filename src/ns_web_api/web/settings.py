# coding: utf-8
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# load dotenv in the base root
from dotenv import load_dotenv, find_dotenv

APP_ROOT = os.path.dirname(__file__)
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path, override=True)

# Build Flask app
app = Flask(__name__, template_folder='templates')

# this may have to change with environment variable
app.config.from_object(os.getenv('CONFIG_ENVIRONMENT', 'config.DevelopmentConfig'))

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', '') # 'postgresql://admin:1qaz2wsx@localhost/'
app.config['DEFAULT_GAME_NAME']= os.getenv('DEFAULT_GAME_NAME', 'Splatoon 2') 
app.config['LINEBOT_CHANNEL_ACCESS_TOKEN']= os.getenv('LINEBOT_CHANNEL_ACCESS_TOKEN', '') 
app.config['LINEBOT_CHANNEL_SECRET']= os.getenv('LINEBOT_CHANNEL_SECRET', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
