import logging

from datetime import datetime
from ..ptx import thsr
from ..events.default import DefaultEvent

logger = logging.getLogger('flask.app')


class TrafficEvent(DefaultEvent):
    """ 交通事件
    """

    def __init__(self):
        super().__init__()

    def occurs(self, vocabulary, *args, **kwargs):
        """交通事件觸發
        """
        if not vocabulary:
            return

        if "高鐵" in vocabulary:
            logger.info('高鐵')
            return self.__thsr_event(vocabulary)

        elif "台鐵" in vocabulary:
            logger.info("traffic-台鐵")
        elif "統聯" in vocabulary:
            logger.info("traffic-統聯")
        elif "國光" in vocabulary:
            logger.info("traffic-國光")

        return

    def __thsr_event(self, vocabulary):
        """高鐵事件處理

        Arguments:
            vocabulary {list of string} -- request vocabulary

        Returns:
            [string] -- reply message
        """

        reply_message = ''

        station_dict = thsr.get_station_id(vocabulary)
        departure = ''
        departure_name = ''
        destination = ''
        destination_name = ''
        time = datetime.now()

        # find the location
        for v in vocabulary:
            if not v in station_dict:
                continue

            if not departure:
                logger.info(
                    f'departure {departure} but v {v} {station_dict[v]}')
                departure_name = v
                departure = station_dict[v]
            elif not destination:
                logger.info(
                    f'destination {destination} but v {v} {station_dict[v]}')

                destination_name = v
                destination = station_dict[v]

        logger.info(f'departure {departure}')
        logger.info(f'destination {destination}')
        logger.info(f'time {time}')

        if not departure or not destination or not time:
            return ''

        if not "位" in ''.join(vocabulary):
            return ''

        reply_message = self.__thsr_seat_event(
            departure, departure_name, destination, destination_name, time)

        return reply_message

    def __thsr_seat_event(self, departure, departure_name,
                          destination, destination_name,
                          respect_time):
        """高鐵 - 找還有座位的班次

        Arguments:
            depature {[type]} -- departure station id.
            departure_name {[type]} -- departure station name.
            destination {[type]} -- destination station id.
            destination_name {[type]} -- destination station name.
            respect_time {[type]} -- respect time.

        Returns:
            [type] -- [description]
        """

        reply_message = ''

        # fine the ptx available seat schedule
        seat_timetables = thsr.get_seat(departure)
        if not seat_timetables:
            return ''

        for seat_timetable in seat_timetables[0]['AvailableSeats']:
            depart_time = datetime.strptime(f"{respect_time.date().strftime('%y %m %d')} {seat_timetable['DepartureTime']}",
                                            '%y %m %d %H:%M')
            # find the nearest
            if depart_time < respect_time:
                continue

            for stop_station in seat_timetable['StopStations']:
                if stop_station['StationID'] != destination:
                    continue

                if stop_station['StandardSeatStatus'].lower() != 'available':
                    continue

                # get it !
                reply_message = f"高鐵班次 {seat_timetable['TrainNo']} 尚有座位\n "
                reply_message += f"從 {departure_name} {seat_timetable['DepartureTime']} 到 {destination_name} \n "
                return reply_message

        return reply_message
