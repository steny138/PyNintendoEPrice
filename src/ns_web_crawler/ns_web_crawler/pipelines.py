# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
from ns_web_crawler.connections import postgresql_conn
from ns_web_crawler.models.game_model import GameModel


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
        if spider.name == "gamer-ns-games":
            if item["name_english"]:
                logging.info("update game name: %s",
                             item["name_english"].strip())
                filter_name = item["name_english"].strip()
                self.session \
                    .query(GameModel) \
                    .filter_by(name=filter_name) \
                    .update(dict(name_tw=item["name_chinese"],
                                 name_en=item["name_english"],
                                 name_jp=item["name_japaness"]))

        self.session.commit()

        return item
