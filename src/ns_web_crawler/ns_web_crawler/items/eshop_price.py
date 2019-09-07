# -*- coding: utf-8 -*-

import scrapy

class EshopProductItem(scrapy.Item):
    nsuid        = scrapy.Field()
    name         = scrapy.Field()
    category     = scrapy.Field()
    prices       = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)