import jieba
import re
import os
from ns_web_api.settings import create_app
from ns_web_api.models import Game
from ns_web_api.rate import CurrencyRate
from ns_web_api.events.analyzer import analyzer
from ns_web_api.viewmodels.game import GameViewModel
from ns_web_api.mask import mask_api_blueprint
from ns_web_api.linebot_apis import line_bot_api_blueprint
from ns_web_api.clinic_apis import clinic_api_blueprint
from ns_web_api.music_api import music_api_blueprint
from ns_web_api.line_liff import line_liff_blueprint

from flask import render_template, send_from_directory

app, db, bootstrap = create_app()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/', defaults={'category': 'named'})
@app.route('/games/', defaults={'category': None})
@app.route('/games/<category>/')
def games(category):
    """遊戲列表頁
    """
    items = Game.query.distinct(Game.name)

    if category == "named":
        items = items.filter(Game.name_tw is not None)
    elif category:
        items = items.filter(Game.name_tw == category or Game.name == category)

    return render_template('games.html')


@app.route("/find/<message>")
def find_message(message):
    """測試傳入訊息jieba分段
    """
    seg_list = ", ".join(jieba.cut(message)).split(', ')
    match_event_message = analyzer.match(seg_list)
    if match_event_message:
        return ''.join(filter(lambda x: x is not None, match_event_message))

    return "hello world"


@app.route('/<game_name>')
def eprice(game_name):
    """遊戲明細頁
    """
    if not game_name:
        game_name = app.config['DEFAULT_GAME_NAME']

    games = Game.query.filter(Game.name == game_name)

    if games.count() == 0:
        if re.search("([\u4e00-\u9fff]{2,}|[a-zA-Z0-9]{4,})", game_name):
            games = Game.query.filter(
                Game.name_tw.ilike(f'%{game_name}%') |
                Game.name.ilike(f'%{game_name}%'))

    currency_rate = CurrencyRate()
    items = []

    for game in games:
        currency = ""

        # get all eprice with this game.
        for key, value in [(key, value) for key, value
                           in game.__dict__.items()]:
            if 'eprice_' not in key:
                continue

            country = key.split('_')[1]
            eprice = value
            currency = game.__dict__[f'currency_{country}']
            onsale = game.__dict__[f'onsale_{country}']

            item = GameViewModel()
            item.name = game.name
            item.name_tw = game.name_tw
            item.country = country.upper()
            item.eprice = eprice or 0
            item.onsale = onsale

            if currency:
                item.eprice = eprice * \
                    currency_rate.caculate_rate(currency, 'TWD')

            if item.eprice > 0:
                items.append(item)

    return render_template('eprice.html',
                           items=sorted(
                               items, key=lambda d: d.eprice, reverse=False),
                           game_name=game_name
                           )


@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()


app.register_blueprint(line_bot_api_blueprint)
app.register_blueprint(mask_api_blueprint)
app.register_blueprint(clinic_api_blueprint)
app.register_blueprint(music_api_blueprint)
app.register_blueprint(line_liff_blueprint)

if __name__ == "__main__":
    app.run()
