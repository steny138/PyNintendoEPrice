import logging
import pytz
import dateutil.parser
from uuid import uuid4
from datetime import datetime

from .eshop.eshop_eu import EShopEUApi
from .eshop.eshop_us import EShopUSApi
from .eshop.eshop_jp import EShopJPApi
from .eshop.eshop_price import EShopPriceApi

from .connections import postgresql_conn
from .models.game_model import GameModel

logger = logging.getLogger(__name__)


class PullNsEshopGame(object):
    def __init__(self, *args):
        super(PullNsEshopGame, self).__init__(*args)
        self.price_api = EShopPriceApi()
        self.countries = ['jp', 'us', 'ca', 'za',
                          'nz', 'nl', 'mx', 'it', 'ch', 'au']

    def pulling(self, eshop_list):
        """ pull the eshop games in eu, us, jp.
        """

        all_games = {}
        # eshop in america
        if 'us' in eshop_list:
            eshop_us = EShopUSApi()

            all_games.update(eshop_us.get_all_games())

        # eshop in europe
        if 'eu' in eshop_list:
            eshop_eu = EShopEUApi()

            all_games.update(eshop_eu.get_all_games())

        # eshop in japan
        if 'jp' in eshop_list:
            eshop_jp = EShopJPApi()

            all_games.update(eshop_jp.get_all_games())

        logger.info(f"found {len(all_games)} games totally.")

        self.all_game_prices = {}
        for game_price in self.__get_all_price(all_games):
            self.all_game_prices.update(game_price)

        logger.info(f"found {len(self.all_game_prices)} game prices totally.")

        session = postgresql_conn.loadSession()

        counter = 0

        try:
            for nid, game in all_games.items():
                if len(game.name) > 100:
                    continue

                if not game.cover:
                    continue

                if not game.cover:
                    continue

                logger.info(f"insert No {counter}. game model")
                counter += 1
                with session.no_autoflush:
                    model = session.query(GameModel) \
                        .filter_by(nsuid=nid) \
                        .first()

                    if not model:
                        model = GameModel(
                            id=uuid4(),
                            nsuid=game.nsuid,
                            code=game.gamecode,
                            name=game.name,
                            category=game.category,
                            cover=game.cover,
                            players=game.players,
                            create_time=datetime.now(),
                            update_time=None
                        )

                    model = self.__pull_price(model)

                    session.add(model)

                    session.commit()

        finally:
            session.close()

    def __pull_price(self, model):

        for country in self.countries:
            key = f'{country.upper()}-{model.nsuid}'
            if not key in self.all_game_prices:
                continue

            price = self.all_game_prices[key]

            if model.nsuid.strip() != str(price['title_id']).strip():
                logger.info(f"{model.nsuid} not equal {price['title_id']}")
                continue

            if 'regular_price' not in price:
                continue

            update_dit = {}
            update_dit['onsale_'+country] = False
            update_dit['currency_' +
                       country] = price['regular_price']['currency']
            update_dit['eprice_'+country] = price['regular_price']['raw_value']

            # discount price onsale in time range.
            if 'discount_price' in price:
                start = dateutil.parser.parse(
                    price['discount_price']['start_datetime']).replace(tzinfo=pytz.timezone('UTC'))
                end = dateutil.parser.parse(price['discount_price']['end_datetime']).replace(
                    tzinfo=pytz.timezone('UTC'))
                now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))

                if start <= now <= end:
                    update_dit['onsale_'+country] = True
                    update_dit['currency_' +
                               country] = price['discount_price']['currency']
                    update_dit['eprice_' +
                               country] = price['discount_price']['raw_value']

            for key, value in update_dit.items():
                setattr(model, key, value)

            # update the model __dict__ cannot trigger sqlalchemy update attribute work,
            # so we got to use setattr to fix this problem.
            # model.__dict__.update(update_dit)

        return model

    def __get_all_price(self, all_games):
        all_nsuids = [value.nsuid for key, value in all_games.items()]

        nsuid_groups = [all_nsuids[x:x+50]
                        for x in range(0, len(all_nsuids), 50)]

        for nsuids in nsuid_groups:

            for country in self.countries:
                # get 50 games per county for once api reuslt
                game_price_dict = self.price_api.get_price(
                    country.upper(), nsuids)

                # list slice rule => [start:stop:step]
                show_id = '~'.join(nsuids[::len(nsuids)-1])
                logger.info(
                    f"{show_id}-{country.upper()} found {len(game_price_dict)} games totally.")

                yield game_price_dict

    @staticmethod
    def startup():
        """startup pulling ns eshop games

        It will pull us, eu, jp region games.
        """
        puller = PullNsEshopGame()

        puller.pulling(['us', 'eu', 'jp'])


if __name__ == '__main__':
    PullNsEshopGame.startup()
