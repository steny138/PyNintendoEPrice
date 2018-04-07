# -*- coding: utf-8 -*-

import scrapy

class CountryCurrencyItem(scrapy.Item):
    country = scrapy.Field()
    country_name = scrapy.Field()
    currency = scrapy.Field()
    currency_name = scrapy.Field()
    symbol = scrapy.Field()
    unit = scrapy.Field()
    digit = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

