# -*- coding: utf-8 -*-

import re
import scrapy
import datetime 
import logging
from ns_web_crawler.items.ns_game_name import NsGameNameItem

class EshopPriceSpider(scrapy.Spider):
    name = "gamer-ns-games"
    def start_requests(self):
        urls = [
            'https://acg.gamer.com.tw/index.php?page=1&p=NS'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # find all games
        games = response.css('div.ACG-mainbox1')        

        for game_dom in games:
            if not game_dom:
                continue
            
            game = NsGameNameItem()
            cover_dom = game_dom.css("div.ACG-mainbox2 > div.ACG-mainbox2A > div.ACG-mainbox2B > a > img")
            game_names = cover_dom.css("::attr(title)").extract_first().strip()
            nameDict = self.parse_game_names(game_names)

            name_type = response.css("div.ACG-mainbox2 ul li::text").extract_first().strip()

            game["game_names"] = game_names
            game["name_chinese"] =  nameDict["name_tw"]
            game["name_japaness"] = nameDict["name_jp"]
            game["name_english"] = nameDict["name_en"]
            game["cover"] = cover_dom.css("::attr(src)").extract_first()
            game["up_date"] = name_type.split("/")[1] if len(name_type.split('/')) > 1 else ""
            
            logging.info("game:%s" % game["name_english"])

            yield game

        now_page = response.css("div#BH-pagebtn p.BH-pagebtnA a.pagenow::text").extract_first()
        last_page = response.css("div#BH-pagebtn p.BH-pagebtnA a:last-child::text").extract_first()

        if now_page:
            if int(now_page) < int(last_page):
                next_page = int(now_page) + 1
                next_page_url = "https://acg.gamer.com.tw/index.php?page=%d&p=NS" % (next_page)
                logging.info("Ready to crawl %s", next_page_url)

                yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_game_names(self, names):
        """separate names string with ',' symbol, 
        that can get the different language names of this game.
        
        Arguments:
            names {string} -- all the language names of this game.
        
        Returns:
            dictionary -- different language names dictionary.
        """

        result = {}
        result["name_en"] = ""
        result["name_jp"] = ""
        result["name_tw"] = ""

        if not names:
            return result

        name_list = names.split(',')

        if len(name_list) >= 3:
            # 瑪利歐 ＋ 瘋狂兔子 王國之戰,マリオ＋ラビッツ キングダムバトル,Mario + Rabbids Kingdom Battle
            result["name_en"] = name_list[2].strip()
            result["name_jp"] = name_list[1].strip()
            result["name_tw"] = name_list[0].strip()
        elif len(name_list) >= 2:

            if re.match("u\"[\u3040-\u309f]+", name_list[1].strip()):
                # 日文
                result["name_jp"] = name_list[1].strip()
            else:
                result["name_en"] = name_list[1].strip()

            
            result["name_tw"] = name_list[0].strip()
        else:
            result["name_tw"] = names
            result["name_en"] = names

        return result







    