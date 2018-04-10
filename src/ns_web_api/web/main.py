# -*- coding: utf-8 -*-

from flask import Flask,render_template
from flask.ext.bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import Eprice,CountryCurrency
app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:1qaz2wsx@localhost/'

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

@app.route("/")
def eprice():
    items = Eprice.query.filter(Eprice.name == 'Splatoon 2')
    return render_template('eprice.html',
        items = items
    )
@app.route("/currency")
def currency():
    items = CountryCurrency.query.all()
    return render_template('currency.html',
        items = items
    )

if __name__ == "__main__":
    app.run()