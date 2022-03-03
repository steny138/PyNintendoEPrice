import os
from flask import Flask
from flask_bootstrap import Bootstrap

# load dotenv in the base root
from dotenv import load_dotenv
from ns_web_api.models import db
from ns_web_api.main import main_api_blueprint
from ns_web_api.mask import mask_api_blueprint
from ns_web_api.linebot_apis import line_bot_api_blueprint
from ns_web_api.clinic_apis import clinic_api_blueprint
from ns_web_api.music_api import music_api_blueprint
from ns_web_api.line_liff import line_liff_blueprint
from ns_web_api.cache import cache_client

APP_ROOT = os.path.dirname(__file__)
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path, override=True)


def create_app():
    app_name = 'flask.app'
    app = Flask(app_name,
                root_path=APP_ROOT,
                template_folder='templates',
                static_url_path='/static')
    print(f'!!! flask app logger name is: {app_name} !!!')

    # this may have to change with environment variable
    app.config.from_object('ns_web_api.config.DevelopmentConfig')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', '')
    app.config['DEFAULT_GAME_NAME'] = os.getenv(
        'DEFAULT_GAME_NAME', 'Splatoon 2')
    app.config['LINEBOT_CHANNEL_ACCESS_TOKEN'] = os.getenv(
        'LINEBOT_CHANNEL_ACCESS_TOKEN', '')
    app.config['LINEBOT_CHANNEL_SECRET'] = os.getenv(
        'LINEBOT_CHANNEL_SECRET', '')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['REDIS_HOST'] = os.getenv('REDIS_HOST', '')
    app.config['REDIS_PORT'] = os.getenv('REDIS_PORT', '')
    app.config['REDIS_PASSWORD'] = os.getenv('REDIS_PASSWORD', '')
    app.config['SPOTIFY_CLIENT_ID'] = os.getenv('SPOTIFY_CLIENT_ID', '')
    app.config['SPOTIFY_CLIENT_SECRET'] = os.getenv(
        'SPOTIFY_CLIENT_SECRET', '')
    app.config['SPOTIFY_AUTH_REDIRECT_URI'] = os.getenv(
        'SPOTIFY_AUTH_REDIRECT_URI', '')
    app.config['YOUTUBE_API_KEY'] = os.getenv('YOUTUBE_API_KEY', '')
    app.config['LINE_LIFF_ID'] = os.getenv('LINE_LIFF_ID', '')

    # register blue print
    app.register_blueprint(main_api_blueprint)
    app.register_blueprint(line_bot_api_blueprint)
    app.register_blueprint(mask_api_blueprint)
    app.register_blueprint(clinic_api_blueprint)
    app.register_blueprint(music_api_blueprint)
    app.register_blueprint(line_liff_blueprint)

    bootstrap = Bootstrap(app)

    db.init_app(app)

    cache_client.init_app(app, config={'CACHE_TYPE': 'simple'})

    return app, bootstrap


app, bootstrap = create_app()
