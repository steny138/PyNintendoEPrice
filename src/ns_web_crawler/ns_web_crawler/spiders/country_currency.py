
# -*- coding: utf-8 -*-

import re
import scrapy
import datetime 
from ns_web_crawler.items.country_currency import CountryCurrencyItem

class CountryCurrnecySpider(scrapy.Spider):
    name = "wiki-country-currency"
    def start_requests(self):
        urls = [
            'https://zh.wikipedia.org/zh-tw/%E6%B5%81%E9%80%9A%E8%B2%A8%E5%B9%A3%E5%88%97%E8%A1%A8'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(response.text)
        # find table include class wikitable that is world regions
        regions = response.css('table.wikitable > tr')
        # print(regions.extract()[0])
        # find table has 6th column
        for index, region_row in enumerate(regions):
            tds = region_row.css('td')
            if len(tds) != 6:
                continue
                
            result = CountryCurrencyItem()
            result["country"] = ""
            result["country_name"] = tds[0].css('a::text').extract_first().strip()
            result["currency"] = tds[3].css('::text').extract_first().strip()
            result["currency_name"] = tds[1].css('a::text').extract_first().strip()
            result["symbol"] = tds[2].css('::text').extract_first()
            result["unit"] = tds[4].css('a::text').extract_first()
            result["digit"] = tds[5].css('::text').extract_first()
            result["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            yield result

        # link to country page to find country code


