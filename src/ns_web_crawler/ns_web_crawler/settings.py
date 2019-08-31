# -*- coding: utf-8 -*-

# load dotenv in the base root
import os

from dotenv import find_dotenv, load_dotenv

APP_ROOT = os.path.dirname(__file__)
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path, override=True)

# Scrapy settings for ns_web_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ns_web_crawler'

SPIDER_MODULES = ['ns_web_crawler.spiders']
NEWSPIDER_MODULE = 'ns_web_crawler.spiders'

LOG_LEVEL= "INFO"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ns_web_crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The delay unit is second.
DOWNLOAD_DELAY = 1

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ns_web_crawler.middlewares.NsWebCrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'ns_web_crawler.middlewares.RandomUserAgentMiddleware': 400
    # 'ns_web_crawler.middlewares.NsWebCrawlerDownloaderMiddleware': None,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'ns_web_crawler.pipelines.PostgreSqlPipeline': 300,
#    'ns_web_crawler.pipeline_storage.google_sheet_pipeline.GoogleSheetApiPipeline': 310
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Database Connection
DATABASE_URL = os.getenv('DATABASE_URL', '')

SPREADSHEET = os.getenv('SPREADSHEET', '')

# Nintendo Settings
US_ALGOLIA_ID      = os.getenv('US_ALGOLIA_ID', 'U3B6GR4UA3')
US_ALGOLIA_KEY     = os.getenv('US_ALGOLIA_KEY', '9a20c93440cf63cf1a7008d75f7438bf')
US_GET_GAMES_URL   = os.getenv('US_GET_GAMES_URL', f'https://{US_ALGOLIA_ID}-dsn.algolia.net/1/indexes/*/queries')
US_GAME_CHECK_CODE = os.getenv('US_GAME_CHECK_CODE', '70010000000185')

EU_GET_GAMES_URL   = os.getenv('EU_GET_GAMES_URL', 'http://search.nintendo-europe.com/{locale}/select')
EU_GAME_CHECK_CODE = os.getenv('EU_GAME_CHECK_CODE', '70010000000184')

JP_GET_GAMES_CURRENT = os.getenv('JP_GET_GAMES_CURRENT', 'https://www.nintendo.co.jp/data/software/xml-system/switch-onsale.xml')
JP_GET_GAMES_COMING  = os.getenv('JP_GET_GAMES_COMING', 'https://www.nintendo.co.jp/data/software/xml-system/switch-coming.xml')
JP_GAME_CHECK_CODE   = os.getenv('JP_GAME_CHECK_CODE', '70010000000039')

PRICE_GET_URL = os.getenv('PRICE_GET_URL', 'https://api.ec.nintendo.com/v1/price')
