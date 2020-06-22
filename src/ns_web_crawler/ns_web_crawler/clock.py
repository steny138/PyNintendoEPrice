# -*- coding: utf-8 -*-

""" 無法用import的方式加入spider class的原因
因為若用scrapy crawl 的指令方式，scrapy 會自動用sys.path.append 將project path加進sys.path
但若用python spider_runner.py 的方式就會找不到路徑
最後得到錯誤 ImportErrored: Not module named xxx...
"""

import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from . import spider_runner
sched = BlockingScheduler()

@sched.scheduled_job('cron', hour='5', minute=10)
def startup():
    spider_runner.startup()

if __name__ == '__main__':
    sched.start()