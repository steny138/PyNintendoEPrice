# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from uuid import uuid4
from datetime import datetime
from ns_web_crawler.connections import postgresql_conn
from ns_web_crawler.models.game_eprice_model import GameEPriceModel
class NsWebCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

# sqlite
# uniqlite
# PostgreSQL
# mongodb
class JsonPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

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
        
        for game in item["games"]:
            for price in game["prices"]:
                model = GameEPriceModel(
                    id = uuid4(),
                    name = game["name"],
                    country = price["country"]["name"],
                    eprice=price["price"],
                    name_tw=None,
                    create_time= datetime.now(),
                    update_time = item["last_updated"]
                )
                self.session.add(model)

        self.session.commit()

        return item
