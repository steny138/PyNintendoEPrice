# coding: utf-8
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# load dotenv in the base root
from dotenv import load_dotenv

APP_ROOT = os.path.dirname(__file__)
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path, override=True)

# Build Flask app
app_name = 'flask.main'
app = Flask(app_name, template_folder='templates',
            static_url_path='/static')

print(f'!!! flask app logger name is: {app_name} !!!')

# this may have to change with environment variable
app.config.from_object(
    os.getenv('CONFIG_ENVIRONMENT', 'config.DevelopmentConfig'))

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', '')
app.config['DEFAULT_GAME_NAME'] = os.getenv('DEFAULT_GAME_NAME', 'Splatoon 2')
app.config['LINEBOT_CHANNEL_ACCESS_TOKEN'] = os.getenv(
    'LINEBOT_CHANNEL_ACCESS_TOKEN', '')
app.config['LINEBOT_CHANNEL_SECRET'] = os.getenv('LINEBOT_CHANNEL_SECRET', '')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['REDIS_HOST'] = os.getenv('REDIS_HOST', '')
app.config['REDIS_PORT'] = os.getenv('REDIS_PORT', '')
app.config['REDIS_PASSWORD'] = os.getenv('REDIS_PASSWORD', '')
app.config['SPOTIFY_CLIENT_ID'] = os.getenv('SPOTIFY_CLIENT_ID', '')
app.config['SPOTIFY_CLIENT_SECRET'] = os.getenv('SPOTIFY_CLIENT_SECRET', '')
app.config['SPOTIFY_AUTH_REDIRECT_URI'] = os.getenv(
    'SPOTIFY_AUTH_REDIRECT_URI', '')
app.config['YOUTUBE_API_KEY'] = os.getenv('YOUTUBE_API_KEY', '')

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)
