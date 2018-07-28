# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, send_from_directory
from models import Eprice,CountryCurrency
from rate import CurrencyRate
from settings import db,app
from bot.events.analyzer import analyzer

import jieba

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', defaults={'category': 'named'})
@app.route('/games/', defaults={'category': None})
@app.route('/games/<category>/')
def games(category):
    items = Eprice.query.distinct(Eprice.name)

    if category == "named":
        items = items.filter(Eprice.name_tw != None)
    elif category:
        items = items.filter(Eprice.name_tw == category or Eprice.name == category)

    return render_template('games.html',
        items = items
    )

@app.route("/currency")
def currency():
    items = CountryCurrency.query.all()
    return render_template('currency.html',
        items = items
    )

@app.route("/find/<message>")
def find_game(message):
    
    seg_list = ", ".join(jieba.cut(message)).split(', ')
    match_event_message = analyzer.match(seg_list)
    if match_event_message:
        return ''.join(filter(lambda x: x is not None, match_event_message))

    return "hello world"
    
@app.route('/<game_name>')
def eprice(game_name):
    if not game_name:
        game_name = app.config['DEFAULT_GAME_NAME']
    
    items = Eprice.query.filter(Eprice.name == game_name)

    currency_rate = CurrencyRate()
    for item in items:
        currency = ""

        if item.currency_specified:
            currency = item.currency_specified
        else:
            country = CountryCurrency.query.filter(CountryCurrency.country == item.country).first()
            if country:
                currency = country.currency
        
        if currency:
            item.eprice = item.eprice * currency_rate.caculate_rate(currency, 'TWD')
            
    return render_template('eprice.html',
        items = sorted(items, key=lambda d: d.eprice, reverse=False),
        game_name = game_name
    )

@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

from linebot_apis import line_bot_api_blueprint
app.register_blueprint(line_bot_api_blueprint)

if __name__ == "__main__":
    app.run()