# -*- coding: utf-8 -*-

from flask.ext.cache import Cache
from settings import app

# Check Configuring Flask-Cache section for more details
cache = Cache(app,config={'CACHE_TYPE': 'simple'})