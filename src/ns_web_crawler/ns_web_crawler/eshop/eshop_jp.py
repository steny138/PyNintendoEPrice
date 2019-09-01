import os
import json
import requests
import xmltodict
from urllib.parse import urlsplit, urlparse,unquote

JP_GET_GAMES_CURRENT = os.getenv('JP_GET_GAMES_CURRENT', 'https://www.nintendo.co.jp/data/software/xml-system/switch-onsale.xml')
JP_GET_GAMES_COMING  = os.getenv('JP_GET_GAMES_COMING', 'https://www.nintendo.co.jp/data/software/xml-system/switch-coming.xml')
JP_GAME_CHECK_CODE   = os.getenv('JP_GAME_CHECK_CODE', '70010000000039')


class EShopJPApi(object):
    def __init__(self, *args):
        pass

    def get_all_games(self):
        """Get all games in japan.
        """
        all_games = {}

        current_games = self.__get_current_games()
        for current_game in current_games['TitleInfoList']['TitleInfo']:
            path = urlparse(current_game['LinkURL']).path
            head, gameid = os.path.split(path)

            if not gameid in all_games :
                print(current_game['TitleName'])
                all_games[gameid] = current_game

        coming_games = self.__get_coming_games()
        for coming_game in coming_games['TitleInfoList']['TitleInfo']:
            path = urlparse(current_game['LinkURL']).path
            head, gameid = os.path.split(path)
            
            if not gameid in all_games :
                print(coming_game['TitleName'])
                all_games[gameid] = coming_game

        print(len(all_games))

    
    def __get_current_games(self):
        r = requests.get(JP_GET_GAMES_CURRENT)
        r.encoding = 'utf-8'
        dict = xmltodict.parse(r.text)

        return dict

    def __get_coming_games(self):
        r = requests.get(JP_GET_GAMES_CURRENT)
        r.encoding = 'utf-8'
        dict = xmltodict.parse(r.text)

        return dict

if __name__ == '__main__':
    req = EShopJPApi()
    req.get_all_games()
