from flask import g, current_app as app
from ns_web_api import db


def get_db():
    with app.app_context():
        if 'db' not in g:
            g.db = db
        return g.db


def close_db():
    with app.app_context():
        db = g.pop('db', None)

        if db is not None:
            db.close()
