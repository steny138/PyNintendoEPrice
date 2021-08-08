from models import Game
from rate import CurrencyRate
from events.default import DefaultEvent


class GamesEvent(DefaultEvent):
    """ 遊戲事件
    """

    def __init__(self):
        super().__init__()

    def occurs(self, message, *args, **kwargs):
        """遊戲事件觸發
        """
        if not message:
            return

        if "找" in message:
            idx = message.index('找')
            if len(message) > idx:
                game_name = "".join(message[idx+1:])
                return self.find_game(game_name)

        elif "玩" in message:
            print("game-玩")

        return

    def find_game(self, game_name):
        items = Game.query \
            .filter(Game.name == game_name) \
            .order_by(Game.name, Game.eprice_us)

        if items:
            currency_rate = CurrencyRate()
            reply_message = "{0}: 有以下價格\n".format(game_name)
            # for item in items:
            #     currency = ""

            #     if item.currency_specified:
            #         currency = item.currency_specified
            #     else:
            #         country = CountryCurrency.query.filter(CountryCurrency.country == item.country).first()
            #         if country:
            #             currency = country.currency

            #     if currency:
            #         item.eprice = item.eprice * currency_rate.caculate_rate(currency, 'TWD')

            #     reply_message += "[{country}: {eprice:.0f}]\n".format(country=item.country, eprice=item.eprice)

            return reply_message
