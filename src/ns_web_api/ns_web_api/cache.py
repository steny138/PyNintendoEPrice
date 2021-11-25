# -*- coding: utf-8 -*-

from flask_caching import Cache
from settings import app

# Check Configuring Flask-Cache section for more details
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
distribute_cache = Cache(app, config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_PASSWORD': app.config['REDIS_PASSWORD'],
    'CACHE_REDIS_HOST': app.config['REDIS_HOST'],
    'CACHE_REDIS_PORT': app.config['REDIS_PORT'],
    'CACHE_KEY_PREFIX': 'LYC_SITE:'})


def append_clinic_cache(doctor, reserve_info):

    # expired time is 8 hours
    key = f'clinic:{doctor}'
    reserve_info_list = distribute_cache.get(key)
    reserve_info_list = reserve_info_list \
        if reserve_info_list is not None else []

    reserve_info_list.append(reserve_info)

    distribute_cache.set(key, reserve_info_list, timeout=60*60*8)


def replace_clinic_cache(doctor, reserve_info_list):
    distribute_cache.set(f'clinic:{doctor}', reserve_info_list, timeout=60*30)
