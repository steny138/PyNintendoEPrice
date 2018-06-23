# -*- coding: utf-8 -*-

import re
import scrapy
import datetime 
import logging
from ns_web_crawler.items.eshop_price_onsale import EshopOnsaleItem

class EshopPriceOnsaleSpider(scrapy.Spider):
    name = "eshop-price-onsale"
    def start_requests(self):

        # 省空間...這些國家先暫時不轉
        self.exclude_country = {
            "BEL", "BGR", "AUT", "HRV", "CYP", 
            "CZE", "FIN", "EST", "GRC", "HUN", 
            "IRL", "ITA", "LVA", "LTU", "LUX", 
            "MLT", "NLD", "NOR", "POL", "PRT", 
            "ROU", "RUS", "SVK", "SVN", "ESP",
            "SWE", "CHE", "GBR"}

        urls = [
            'https://eshop-prices.com/?currency=USD'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # find all games
        main = response.css('div.prices > table[data-search-table]')
        countries_dom = main.css('thead > tr > th[title]')
        games_dom = main.css('tbody > tr[data-table-searchable]')
        self.countries = []

        # 須事先搜集國家相關代碼與名稱
        for country_dom in countries_dom:
            country = self.get_country_item(country_dom)

            if not country:
                continue
                
            if not country["code"]:
                continue

            if country["code"] in self.exclude_country:
                continue
            
            self.countries.append(country)

        logging.info('eshop has game count : %d', len(games_dom))
        
        for game_dom in games_dom:
            
            if game_dom.css("th > a > span.game-serie").extract_first():
                continue

            name = game_dom.css("th > a::text").extract_first().strip()
            url = game_dom.css("th > a::attr(href)").extract_first().strip()
            yield scrapy.Request(url, callback=self.parse_detail)
    
    def get_country_item(self, th):
        country = {}
        country["name"] = th.css("th::attr(title)").extract_first()
        country["code"] = th.css("::text").extract_first().strip()

        return country

    def parse_detail(self, response):
        main = response.css('div.wrapper > div.well > table')
        prices_dom = main.css('tr')
        game_name = response.css('div.game-hero > div.wrapper > div h1::text').extract_first().strip()

        for price_tr in prices_dom:
            if price_tr.css('th.price-position').extract_first():
                continue
            country_name = price_tr.xpath('td[2]/text()').extract_first().strip()
            
            find_country = [x for x in self.countries if x["name"] == country_name]
            country = next(iter(find_country), None) 
            if country is None:
                continue

            price = EshopOnsaleItem()
            price["name"] = game_name
            price["country"] = country["code"]
            price["currency"] = "USD" # because querystring is based on USD
            price["price"] = price_tr.css('td.price-value::text').extract_first().strip().replace("$", "")

            if price_tr.css('td.price-meta > span::attr(title)').extract_first():
                price["onsale"] = "On sale" in price_tr.css('td.price-meta > span::attr(title)').extract_first().strip()
            else:
                price["onsale"] = False    

            yield price