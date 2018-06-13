# -*- coding: utf-8 -*-

""" 無法用import的方式加入spider class的原因
因為若用scrapy crawl 的指令方式，scrapy 會自動用sys.path.append 將project path加進sys.path
但若用python spider_runner.py 的方式就會找不到路徑
最後得到錯誤 ImportErrored: Not module named xxx...
"""

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

configure_logging()
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks
def crawl():
    yield runner.crawl("eshop-price-index")
    yield runner.crawl("wiki-country-currency")
    yield runner.crawl("gamer-ns-games")
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished