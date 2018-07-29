
import requests

class TrafficEvent(object):
    """ 交通事件
    """

    def __init__(self):
        pass

    def occurs(self, vocabulary):
        """交通事件觸發
        """
        if not vocabulary:
            return
        
        if "高鐵" in vocabulary:
            print("traffic-高鐵")            
        elif "台鐵" in vocabulary:
            print("traffic-台鐵")
        elif "統聯" in vocabulary:
            print("traffic-統聯")
        elif "國光" in vocabulary:
            print("traffic-國光")
        
        return

if __name__ == "__main__":
    traffic_event = TrafficEvent()