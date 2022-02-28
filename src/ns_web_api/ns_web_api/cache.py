# -*- coding: utf-8 -*-

from flask import g
from werkzeug.local import LocalProxy

# Check Configuring Flask-Cache section for more details


def get_cache():
    if 'db' not in g:
        pass
    return g.cache


def get_distribute_cache():
    if 'distribute_cache' not in g:
        pass
    return g.distribute_cache


cache = LocalProxy(get_cache)
distribute_cache = LocalProxy(get_distribute_cache)


def append_clinic_cache(doctor, reserve_info):

    # expired time is 8 hours
    key = f'clinic:{doctor}'
    reserve_info_list = distribute_cache.get(key)
    reserve_info_list = reserve_info_list \
        if reserve_info_list is not None else []

    reserve_info_list.append(reserve_info)

    distribute_cache.set(key, reserve_info_list, timeout=60*60*8)


def replace_clinic_cache(doctor, reserve_info_list):
    distribute_cache.set(
        f'clinic:{doctor}', reserve_info_list, timeout=60*30)
