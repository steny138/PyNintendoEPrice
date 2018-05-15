# -*- coding: utf-8 -*-

import re
import scrapy
import datetime 
import logging
from ns_web_crawler.items.eshop_price import EshopPriceItem, EshopProductItem, EshopPriceCountryItem

class EshopPriceSpider(scrapy.Spider):
    name = "eshop-price-index"
    def start_requests(self):
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

        result = EshopPriceItem()
        result["games"] = []
        result["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        countries = []

        for country_dom in countries_dom:
            country = self.get_country_item(country_dom)

            if not country:
                continue
                
            if not country["code"]:
                continue
            
            countries.append(country)

        for game_dom in games_dom:
            game = self.get_game_item(game_dom, countries)
            
            if not game:
                continue
            
            result["games"].append(game)

            logging.info("find the game: %s", game["name"])

        yield result

    
    def get_country_item(self, th):
        country = {}
        country["code"] = th.css("th::attr(title)").extract_first()
        country["name"] = th.css("::text").extract_first().strip()

        return country
    
    def get_game_item(self, tr, countries):
        game = EshopProductItem()
        game["name"] = tr.css("th > a::text").extract_first().strip()
        game["prices"] = []

        tds = tr.css("td")

        for index, game_td in enumerate(tds):

            if not len(countries) > index:
                continue

            game_price = self.get_game_price_item(game_td, countries[index])

            if not game_price:
                continue

            game["prices"].append(game_price)

        return game

    def get_game_price_item(self, td, country):
        price = EshopPriceCountryItem()

        price_text = re.findall("\d+\.\d+", td.css("::text").extract_first().strip())

        if not price_text:
            return None

        price["country"] = country
        price["currency"] = "USD" # because querystring is based on USD
        price["price"] = price_text[0]
        price["onsale"] = td.css('.l').extract_first() is not None
        return price

