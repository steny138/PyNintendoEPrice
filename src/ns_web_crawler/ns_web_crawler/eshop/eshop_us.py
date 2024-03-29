import requests
import copy
import logging
from urllib.parse import urlencode, quote

from .game_poco import EshopGame
from .eshop_costants import check_nsuid

# from .. import settings

import os
US_ALGOLIA_ID = os.getenv('US_ALGOLIA_ID', 'U3B6GR4UA3')
US_ALGOLIA_KEY = os.getenv(
    'US_ALGOLIA_KEY', 'c4da8be7fd29f0f5bfa42920b0a99dc7')
US_GET_GAMES_URL = os.getenv(
    'US_GET_GAMES_URL', f'https://{US_ALGOLIA_ID}-dsn.algolia.net/1/indexes/*/queries')
US_GAME_CHECK_CODE = os.getenv('US_GAME_CHECK_CODE', '70010000000185')

logger = logging.getLogger(__name__)


class EShopUSApi(object):
    """The api helper for getting Nintendo US Eshop games.
    """
    US_GET_GAMES_OPTIONS = {
        'system': 'platform:Nintendo Switch', 'sort': 'title', 'direction': 'asc'}
    US_GAME_CODE_REGEX = '/HAC\w(\w{4})/'
    US_GAME_LIST_LIMIT = 100
    US_GAME_QUERY_LIMIT = 1000
    US_PRICE_RANGES = [
        '$5 - $9.99',
        '$10 - $19.99',
        '$20 - $39.99'
        '$40+'
    ]

    QUERYSTRING = {
        'x-algolia-application-id': US_ALGOLIA_ID,
        'x-algolia-api-key': US_ALGOLIA_KEY
    }

    default_parameters = {
        'query': '',
        'facetFilters': [
            [US_GET_GAMES_OPTIONS['system']],
            ['availability:Available now']
        ]
    }

    def __init__(self, *args):
        pass

    def get_all_games(self):
        """Get all eshop games in us.
        """
        categories = self.__get_all_categories()
        all_games = {}
        for category_name, category_game_count in categories.items():

            price_ranges = self.US_PRICE_RANGES

            if category_game_count <= self.US_GAME_QUERY_LIMIT:
                price_ranges = [None]

            for price_range in price_ranges:
                category_games = self.__get_category_games(
                    category_name, price_range)

                if category_games:
                    for game in [category_game for category_game
                                 in category_games
                                 if not category_game['slug'] in all_games]:
                        # no nsuid cannot get eshop price.
                        if 'nsuid' not in game:
                            continue

                        gameid = game['nsuid']
                        if not check_nsuid(gameid):
                            continue

                        cover = ''
                        if 'boxArt' in game:
                            cover = f"https://www.nintendo.com{game['boxArt']}"

                        all_games[gameid] = EshopGame(
                            game.get('nsuid'),
                            game.get('id', 'unrelease'),
                            game.get('title'),
                            'us',
                            cover,
                            ','.join(game.get('genres')),
                            game.get('players'))

        logger.info(f"found {len(all_games)} games in America.")

        return all_games

    def __get_category_games(self, category, price_range):
        """Get all Nintendo US Eshop games
        """
        # query=&hitsPerPage=42&maxValuesPerFacet=30&page=1
        # &tagFilters=&facetFilters=[["platform:Nintendo Switch"],
        # ["availability:Available now"]]
        page = 0
        cursor = 0
        size = self.US_GAME_LIST_LIMIT
        games = []

        while cursor <= (page + 1) * size:
            (current_position, values) = self.__get_api_result(
                category, page, size, price_range)
            if len(values) <= 0:
                logger.info(
                    f"{category}-{price_range} current cursor position: {cursor} has no games")
                break

            page += 1
            cursor = current_position
            games.extend(values)

            logger.info(
                f"{category}-{price_range} current cursor position: {cursor}[{values[0]['title']}]")

        return games

    def __get_api_result(self, category, page, size, price_range=None):
        parameters = copy.deepcopy(self.default_parameters)

        parameters['facetFilters'].append([f'genres:{category}'])
        parameters['facets'] = ["platform", "availability", "genres"]
        parameters['hitsPerPage'] = size
        parameters['page'] = page
        parameters['tagFilters'] = ''
        parameters['maxValuesPerFacet'] = 30
        if price_range:
            parameters['facetFilters'].append([f'priceRange:{price_range}'])

        sort = self.US_GET_GAMES_OPTIONS['sort']
        direction = self.US_GET_GAMES_OPTIONS['direction']

        body = {
            'requests': [
                {
                    'indexName': f'ncom_game_en_us_{sort}_{direction}',
                    'params': urlencode(parameters, quote_via=quote).replace('%27', '%22')
                }
            ]
        }

        r = requests.post(US_GET_GAMES_URL, params=self.QUERYSTRING, json=body)
        result = r.json()['results'][0]
        reponse_values = result['hits']
        hits_page = int(result['page'])
        hits_size = int(result['hitsPerPage'])
        hits_current = len(result['hits'])

        cursor = (hits_page * hits_size) + hits_current

        return (cursor, reponse_values)

    def __get_all_categories(self):
        """因為ALGOLIA搜尋最大上限只給一千
            所以要分遊戲類型做搜尋
            但遊戲類型內的遊戲數量還是有可能超過一千
            所以還要區分價格區間，用兩個條件來取得所有遊戲
        """

        parameters = copy.deepcopy(self.default_parameters)
        parameters['facets'] = ["genres"]
        parameters['hitsPerPage'] = 1

        sort = self.US_GET_GAMES_OPTIONS['sort']
        direction = self.US_GET_GAMES_OPTIONS['direction']

        body = {
            'requests': [
                {
                    'indexName': f'ncom_game_en_us_{sort}_{direction}',
                    'params': urlencode(parameters, quote_via=quote).replace('%27', '%22')
                }
            ]
        }

        r = requests.post(US_GET_GAMES_URL, params=self.QUERYSTRING, json=body)

        return r.json()['results'][0]['facets']['genres']


if __name__ == '__main__':
    req = EShopUSApi()
    req.get_all_games()
