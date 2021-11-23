import logging


class DefaultEvent(object):
    """預設回覆事件
    """

    def __init__(self, *args):
        self.logger = logging.getLogger('flask.app')

    def occurs(self, *args, **kwargs):
        self.logger.debug(f'occurs at {self.__class__.__name__}')
