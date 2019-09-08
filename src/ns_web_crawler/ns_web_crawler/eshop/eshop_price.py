
import requests
import json


import os
PRICE_GET_URL = os.getenv('PRICE_GET_URL', 'https://api.ec.nintendo.com/v1/price')

class EShopPriceApi(object):
    def __init__(self, *args):
        pass

    def get_price(self, country, nsuids):
        all_games_price = {}
        games_price = self.__get_api_result(country, nsuids)

        if not 'prices' in games_price:
            return all_games_price

        for game_price in games_price['prices']:
            gameid = game_price['title_id']
            if not gameid in all_games_price :
                all_games_price[gameid] = games_price
        # nsuid 並非遊戲ＩＤ, 是shop分辨遊戲的id, 故不同shop 同遊戲 會有不同nsuid
        return all_games_price
    
    def __get_api_result(self, country, nsuids):
        querystring = {
            'country': country,
            'lang': 'en',
            'ids': ','.join(nsuids) # 逗點隔開
        }

        r = requests.get(PRICE_GET_URL, params=querystring)
        r.encoding = 'utf-8'
        return r.json()

if __name__ == '__main__':
    req = EShopPriceApi()
    req.get_price('US', ['70010000000185'])