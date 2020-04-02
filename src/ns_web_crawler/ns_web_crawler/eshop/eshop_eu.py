import json
import requests
import logging
import copy
from .game_poco import EshopGame
from .eshop_costants import check_nsuid

import os
EU_GET_GAMES_URL   = os.getenv('EU_GET_GAMES_URL', 'https://search.nintendo-europe.com/{locale}/select')
EU_GAME_CHECK_CODE = os.getenv('EU_GAME_CHECK_CODE', '70010000000184')

logger = logging.getLogger(__name__)

class EShopEUApi(object):
    EU_GET_GAMES_OPTIONS = {
        'fq': 'type:GAME AND ((playable_on_txt:"HAC")) AND sorting_title:* AND *:*',
        'q': '*',
        'sort': 'sorting_title asc',
        'start': '0',
        'wt': 'json',
    }

    EU_DEFAULT_LOCALE = 'en'
    EU_GAME_LIST_LIMIT = 9999

    def __init__(self, *args):
        pass

    def get_all_games(self):
        """Get all games in Europe.
        """
        all_games = {}
        response = self.__get_api_result()
        game_count = response['response']['numFound']
        for game in response['response']['docs']:
            if not 'nsuid_txt' in game:
                continue

            gameid = ''.join(game.get('nsuid_txt'))
            gamecode = ''.join(game.get('product_code_txt', []))
            if check_nsuid(gameid) and not gameid in all_games :

                all_games[gameid] = EshopGame(
                    gameid,
                    gamecode,
                    game.get('title'), 
                    'eu',
                    game.get('image_url'),
                    ','.join(game.get('game_category')),
                    f"{game.get('players_from','0')}-{game.get('players_to', '0')}")
        
        logger.info(f"found {len(all_games)} games in Europe.")

        return all_games
    
    def __get_api_result(self):
        querystring = copy.deepcopy(self.EU_GET_GAMES_OPTIONS)
        querystring['rows'] = self.EU_GAME_LIST_LIMIT

        url = EU_GET_GAMES_URL.replace('{locale}', self.EU_DEFAULT_LOCALE)
        logger.info(f"get eu api {url} with {querystring}")
        
        r = requests.get(url, params=querystring)
        return r.json()


if __name__ == '__main__':
    req = EShopEUApi()
    req.get_all_games()