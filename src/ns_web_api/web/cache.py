# -*- coding: utf-8 -*-

from flask_caching import Cache
from settings import app

# Check Configuring Flask-Cache section for more details
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


def append_clinic_cache(doctor, reserve_info):

    # expired time is 8 hours
    key = f'clinic:{doctor}'
    reserve_info_list = cache.get(key)
    reserve_info_list = reserve_info_list \
        if reserve_info_list is not None else []

    reserve_info_list.append(reserve_info)

    cache.set(key, reserve_info_list, timeout=60*60*8)


def replace_clinic_cache(doctor, reserve_info_list):
    cache.set(f'clinic:{doctor}', reserve_info_list, timeout=60*30)
