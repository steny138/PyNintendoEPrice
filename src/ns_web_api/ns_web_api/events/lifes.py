from ..events.default import DefaultEvent


class LifeEvent(DefaultEvent):
    """ 日常生活事件
    """

    def __init__(self):
        super().__init__()

    def occurs(self, message, *args, **kwargs):
        """日常生活事件觸發
        """
        if not message:
            return

        if "生活" in message:
            pass

        elif "旅遊" in message:
            pass

        return
