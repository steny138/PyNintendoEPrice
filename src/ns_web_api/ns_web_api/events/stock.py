import logging
import twstock
from events.default import DefaultEvent

logger = logging.getLogger('flask.app')


class StockEvent(DefaultEvent):
    """ 股市事件
    """

    def __init__(self):
        super().__init__()

    def occurs(self, vocabulary, *args, **kwargs):
        """股市事件觸發
        """

        if not vocabulary:
            return

        if "股價" in vocabulary:
            logger.info(vocabulary)
            return self.__stock_price_event(vocabulary)

        return

    def __stock_price_event(self, vocabulary):
        """股價事件處理

        Arguments:
            vocabulary {list of string} -- request vocabulary

        Returns:
            [string] -- reply message
        """

        reply_message = ''

        ix = vocabulary.index('*')

        stock_no = vocabulary[ix+1:][0]

        realtime = twstock.realtime.get(stock_no)

        name = realtime["info"]["name"]
        price = realtime["realtime"]["latest_trade_price"]
        if price == "-":
            # get buyer first price replace non trade price
            price = realtime["realtime"]["best_bid_price"][0]

        reply_message = f'{name} 現價 {float(price):.0f}'
        reply_message += self.__reply_volume(realtime)
        return reply_message

    def __reply_volume(self, realtime):
        seller_volume = [int(s)
                         for s in realtime["realtime"]["best_ask_volume"]]

        seller_volume = sum(seller_volume)
        buyer_volume = [int(s)
                        for s in realtime["realtime"]["best_bid_volume"]]
        buyer_volume = sum(buyer_volume)

        if seller_volume > buyer_volume:
            return " 賣壓高漲🚁"
        elif seller_volume < buyer_volume:
            return " 多軍壓境🧨"

        return ""
