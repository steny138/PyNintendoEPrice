# -*- coding: utf-8 -*-

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

configure_logging()

@defer.inlineCallbacks
def crawl_job():
    """
    Job to start spiders.
    Return Deferred, which will execute after crawl has completed.
    """
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    yield runner.crawl("eshop-price-index")
    yield runner.crawl("eshop-price-onsale")
    # yield runner.crawl("wiki-country-currency")
    yield runner.crawl("gamer-ns-games")
    # reactor.stop()
    defer.returnValue('success crawl job')

def schedule_next_crawl(null, sleep_time):
    """
    Schedule the next crawl
    """
    reactor.callLater(sleep_time, crawl)

def crawl():
    """
    A "recursive" function that schedules a crawl specified seconds after
    each successful crawl.
    """
    # crawl_job() returns a Deferred
    d = crawl_job()
    # call schedule_next_crawl(<scrapy response>, n) after crawl job is complete
    # work per day!
    d.addCallback(schedule_next_crawl, 86400)
    d.addErrback(catch_error)

def catch_error(failure):
    print(failure.value)

if __name__=="__main__":
    crawl()
    reactor.run() # the script will block here until the last crawl call is finished