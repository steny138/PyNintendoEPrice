# -*- coding: utf-8 -*-

import scrapy

class NsGameNameItem(scrapy.Item):
    game_names = scrapy.Field()
    name_chinese = scrapy.Field()
    name_japaness = scrapy.Field()
    name_english = scrapy.Field()
    cover = scrapy.Field()
    up_date = scrapy.Field()