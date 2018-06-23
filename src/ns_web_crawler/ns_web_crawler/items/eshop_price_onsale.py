# -*- coding: utf-8 -*-

import scrapy

class EshopOnsaleItem(scrapy.Item):
    name = scrapy.Field()
    country = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    onsale = scrapy.Field()
