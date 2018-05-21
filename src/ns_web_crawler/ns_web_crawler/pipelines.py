# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from uuid import uuid4
from datetime import datetime
from ns_web_crawler.connections import postgresql_conn
from ns_web_crawler.models.game_eprice_model import GameEPriceModel
from ns_web_crawler.models.country_mapping_currency_model import CountryCurrencyModel

class NsWebCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

# sqlite
# uniqlite
# PostgreSQL
# mongodb
class JsonPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class PostgreSqlPipeline(object):

    def open_spider(self, spider):
        self.session = postgresql_conn.loadSession()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        if spider.name == "eshop-price-index":
            for price in item["prices"]:
                model = self.session.query(GameEPriceModel) \
                                    .filter_by(country = price["country"]["name"], name = item["name"]) \
                                    .first()
                if model:
                    model.eprice=price["price"]
                    model.eprice_specified=price["price"]
                    model.currency_specified=price["currency"]
                    model.onsale= price["onsale"]
                    model.update_time = item["last_updated"]
                else:
                    model = GameEPriceModel(
                        id = uuid4(),
                        name = item["name"],
                        country = price["country"]["name"],
                        eprice=price["price"],
                        eprice_specified=price["price"],
                        onsale= price["onsale"],
                        currency_specified=price["currency"],
                        name_tw=None,
                        create_time= datetime.now(),
                        update_time = item["last_updated"]
                    )
                self.session.add(model)
        elif spider.name == "wiki-country-currency":
            model = self.session.query(CountryCurrencyModel).filter_by(country = item["country"],).first()

            if model:
                model.currency = item["currency"]
                model.country_name=item["country_name"]
                model.currency_name=item["currency_name"]
                model.symbol=item["symbol"]
                model.unit=item["unit"]
                model.digit= item["digit"]
                model.last_updated = item["last_updated"]
            else:
                model = CountryCurrencyModel(
                    id = uuid4(),
                    country = item["country"],
                    currency = item["currency"],
                    country_name=item["country_name"],
                    currency_name=item["currency_name"],
                    symbol=item["symbol"],
                    unit=item["unit"],
                    digit= item["digit"],
                    last_updated = item["last_updated"]
                )

            self.session.add(model) 
        elif spider.name == "gamer-ns-games":

            if item["name_english"]:
                logging.info("update game name: %s", item["name_english"].strip())
                filter_name = item["name_english"].strip()
                self.session \
                    .query(GameEPriceModel) \
                    .filter_by(name = filter_name) \
                    .update(dict(name_tw=item["name_chinese"],
                                name_en=item["name_english"],
                                name_jp=item["name_japaness"]))
            
        self.session.commit()

        return item
