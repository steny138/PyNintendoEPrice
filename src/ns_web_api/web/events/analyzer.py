
from .games import GamesEvent
from .lifes import LifeEvent
from .traffic import TrafficEvent

class EventAyalyzer(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(EventAyalyzer, cls).__new__(cls, *args, **kw)  
            cls._instance.events = []

            cls._instance.events.append(GamesEvent())
            cls._instance.events.append(LifeEvent())
            cls._instance.events.append(TrafficEvent())

        return cls._instance 

    def match(self, fragments):
        match_events = [(lambda x: x.occurs(fragments))(x) for x in self.events]
        return match_events

analyzer = EventAyalyzer()