# -*- coding: utf-8 -*-

import scrapy

class EshopProductItem(scrapy.Item):
    name = scrapy.Field()
    prices = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

class EshopPriceCountryItem(scrapy.Item):
    country = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    onsale = scrapy.Field()