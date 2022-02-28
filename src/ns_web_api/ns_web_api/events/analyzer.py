
from .games import GamesEvent
from .lifes import LifeEvent
from .traffic import TrafficEvent
from .diving import DivingEvent
from .stock import StockEvent
from .clinic import ClinicEvent
from .music import MusicEvent
from .baby_naming import BabyNamingEvent


class EventAyalyzer(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(EventAyalyzer, cls).__new__(cls, *args, **kw)
            cls._instance.events = []

            cls._instance.events.append(GamesEvent())
            cls._instance.events.append(LifeEvent())
            cls._instance.events.append(TrafficEvent())
            cls._instance.events.append(DivingEvent())
            cls._instance.events.append(StockEvent())
            cls._instance.events.append(ClinicEvent())
            cls._instance.events.append(MusicEvent())
            cls._instance.events.append(BabyNamingEvent())

        return cls._instance

    def match(self, fragments, *args, **kwargs):
        match_events = [(lambda x: x.occurs(fragments, *args, **kwargs))(x)
                        for x in self.events]

        return list(filter(None, match_events))  # remove empty string


analyzer = EventAyalyzer()
