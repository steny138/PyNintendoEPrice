import logging
import twstock

logger = logging.getLogger('flask.app')


class StockEvent(object):
    """ 股市事件
    """

    def __init__(self):
        pass

    def occurs(self, vocabulary):
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

        return reply_message
