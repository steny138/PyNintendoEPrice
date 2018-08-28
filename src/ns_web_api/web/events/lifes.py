class LifeEvent(object):
    """ 日常生活事件
    """

    def __init__(self):
        pass

    def occurs(self, message):
        """日常生活事件觸發
        """
        if not message:
            return
            
        if "生活" in message:
            pass
            
        elif "旅遊" in message:
            pass
        
        return
