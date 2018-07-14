from models import Eprice

class GamesEvent(object):
    """ 遊戲事件
    """

    def __init__(self):
        pass

    def occurs(self, message):
        """遊戲事件觸發
        """
        print("parameter message is: {0}".format(message))

        if not message:
            return
            
        if "找" in message:
            idx = message.index('找')
            if len(message) > idx:
                game_name = "".join(message[idx+1:])
                item = Eprice.query.filter(Eprice.name == game_name).first()
                print(item.eprice)

            # 中了
            print("game-找")
            
        elif "玩" in message:
            print("game-玩")
        
        return
