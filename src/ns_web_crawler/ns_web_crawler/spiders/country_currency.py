
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

            if tds[0].css('a::attr(href)'):
                yield response.follow(
                    tds[0].css('a::attr(href)').extract_first().replace('wiki', 'zh-tw'), 
                    meta={'item': result},
                    callback=self.parse_country_code)

    def parse_country_code(self, response):

        # link to country page to find country code
        item = response.request.meta['item']
        # countryTd = response.css("table.infobox tr:has(th>a:contains(\"國家代碼\")) td")
        # xpath_condition = ''.join(c for c in u"table[contains(@class, 'infobox')]/tr[contains(.//th//a/text(), '國家代碼')]" if self.valid_xml_char_ordinal(c))
        # countryTd = response.css(css_condition)        
        # countryTd = response.xpath(xpath_condition)
        countryTrs = response.css("table.infobox tr")
        for countryTr in countryTrs:
            # selector cannot find some element for 國家代碼
            # so we make it by ourself.
            if not countryTr.css("th > a::text").extract_first():
                continue
            
            if not countryTr.css("th > a::text").extract_first().strip() == u"國家代碼":
                continue
            
            countryLink = countryTr.css("td::text")
            if countryLink:
                item["country"]  = countryLink.extract_first().split('(')[0]
                if len(item["country"])> 10:
                    item["country"] = ""
            yield item

    def valid_xml_char_ordinal(self, c):
        codepoint = ord(c)
        # conditions ordered by presumed frequency
        return (
            0x20 <= codepoint <= 0xD7FF or
            codepoint in (0x9, 0xA, 0xD) or
            0xE000 <= codepoint <= 0xFFFD or
            0x10000 <= codepoint <= 0x10FFFF
            )