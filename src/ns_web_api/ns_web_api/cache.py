from flask import g, current_app as app
from flask_caching import Cache

cache_client = Cache()


def get_cache():
    with app.app_context():
        if 'cache' not in g:
            g.cache = Cache(app, config={'CACHE_TYPE': 'simple'})
        return g.cache


def get_distribute_cache():
    with app.app_context():
        if 'distribute_cache' not in g:
            g.distribute_cache = Cache(app, config={
                'CACHE_TYPE': 'RedisCache',
                'CACHE_REDIS_PASSWORD': app.config['REDIS_PASSWORD'],
                'CACHE_REDIS_HOST': app.config['REDIS_HOST'],
                'CACHE_REDIS_PORT': app.config['REDIS_PORT'],
                'CACHE_KEY_PREFIX': 'LYC_SITE:'})

        return g.distribute_cache


def append_clinic_cache(doctor, reserve_info):

    distribute_cache = get_distribute_cache()

    # expired time is 8 hours
    key = f'clinic:{doctor}'
    reserve_info_list = distribute_cache.get(key)
    reserve_info_list = reserve_info_list \
        if reserve_info_list is not None else []

    reserve_info_list.append(reserve_info)

    distribute_cache.set(key, reserve_info_list, timeout=60*60*8)


def replace_clinic_cache(doctor, reserve_info_list):
    distribute_cache = get_distribute_cache()

    distribute_cache.set(
        f'clinic:{doctor}', reserve_info_list, timeout=60*30)
