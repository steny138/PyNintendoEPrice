# -*- coding: utf-8 -*-

from flask import Flask,render_template
from models import Eprice,CountryCurrency
from rate import CurrencyRate
from settings import db,app

@app.route('/', defaults={'game_name': None})
@app.route('/<game_name>')
def eprice(game_name):
    print game_name
    if not game_name:
        game_name = 'Splatoon 2'
    
    items = Eprice.query.filter(Eprice.name == game_name)

    currency_rate = CurrencyRate()
    for item in items:
        currency = ""

        if item.currency_specified:
            currency = item.currency_specified
        else:
            country = CountryCurrency.query.filter(CountryCurrency.country == item.country).first()
            if country:
                print item.eprice
                currency = country.currency
        
        if currency:
            item.eprice = item.eprice * currency_rate.caculate_rate(currency, 'TWD')

       
            
    return render_template('eprice.html',
        items = sorted(items, key=lambda d: d.eprice, reverse=False)
    )

@app.route("/currency")
def currency():
    items = CountryCurrency.query.all()
    return render_template('currency.html',
        items = items
    )

if __name__ == "__main__":
    app.run()