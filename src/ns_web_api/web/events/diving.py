import requests
from bs4 import BeautifulSoup
from events.default import DefaultEvent


class DivingEvent(DefaultEvent):
    """ 潛水事件
    """

    def __init__(self):
        super().__init__()
        self.diving_place = [
            '小琉球',
            '墾丁',
            '後壁湖',
            '綠島',
            '蘭嶼',
            '東北角'
        ]

    def occurs(self, vocabulary, *args, **kwargs):
        """潛水事件觸發
        """
        if not vocabulary:
            return

        return_msg = []

        if all(elem in self.diving_place for elem in vocabulary):
            self.logger.info(f'潛點事件處理: {vocabulary}')
            for v in vocabulary:
                return_msg.append(self.__diving_event(v))

        return ', '.join(return_msg)

    def __diving_event(self, vocabulary):
        """潛點事件處理
        """

        sea_id_dict = {
            '小琉球': {
                'temp': 'OSea07',
                'temp_keyword': '小琉球',
                'tidal': 'NSea07',
                'tidal_keyword': '琉球'
            },
            '綠島': {
                'temp': 'OSea10',
                'temp_keyword': '綠島',
                'tidal': 'NSea11',
                'tidal_keyword': '綠島'
            },
            '蘭嶼': {
                'temp': 'OSea10',
                'temp_keyword': '蘭嶼',
                'tidal': 'NSea11',
                'tidal_keyword': '蘭嶼'
            },
            '墾丁': {
                'temp': 'OSea08',
                'temp_keyword': '後壁湖',
                'tidal': 'NSea08',
                'tidal_keyword': '恆春'
            },
            '後壁湖': {
                'temp': 'OSea08',
                'temp_keyword': '後壁湖',
                'tidal': 'NSea08',
                'tidal_keyword': '恆春'
            },
            '東北角': {
                'temp': 'OSea01',
                'temp_keyword': '龍洞',
                'tidal': 'NSea01',
                'tidal_keyword': '萬里'
            }
        }

        sea_id = sea_id_dict.get(vocabulary)

        sea_info = self.__sea_temperature(
            sea_id['temp'], sea_id['temp_keyword'])

        tidal_info = self.__tidal(sea_id['tidal'], sea_id['tidal_keyword'])

        if sea_info or tidal_info:
            return vocabulary + '\n' + sea_info + '\n' + tidal_info

        return f'{vocabulary}查無海流資訊'

    def __sea_temperature(self, sea_id, keyword):
        """
        海溫資訊
        1. sea temperature
        2. wind direction
        """

        url = f'https://www.cwb.gov.tw/V8/C/M/OBS_Marine/48hrsSeaObs_MOD/{sea_id}.html'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.select('tr')

        msg = []
        for row in rows:
            title = row.select_one('th a').getText()
            title = " ".join(title.split())

            if keyword not in title:
                continue

            wind = row.select('td')[5].select_one('span.wind span.sr-only')
            wind_txt = wind.getText() if wind is not None else ''

            temperature = row.select('td')[7].select_one('span.tempC')
            temperature_txt = temperature.getText() if temperature is not None else ''

            if temperature_txt and temperature_txt != '-':
                msg.append(f'風向{" ".join(wind_txt.split())}' +
                           f' 海溫{" ".join(temperature_txt.split())}度')

        if msg:
            return ' '.join(msg)

        return ''

    def __tidal(self, sea_id, keyword):
        """
        潮汐資訊
        """

        url = f'https://www.cwb.gov.tw/V8/C/M/Fishery/tide_MOD/{sea_id}_1.html'

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.select('.table-blueroute tbody')

        msg = []

        for row in rows:
            title = row.select_one(f'#{sea_id}').getText()
            title = " ".join(title.split())

            if keyword not in title:
                continue

            tidal_timetable = row.select(f'td[headers^="{sea_id}"]')

            for tidal_timerow in tidal_timetable:
                text = ''
                if 'tide' in tidal_timerow['headers']:
                    text = tidal_timerow.getText()

                if 'time' in tidal_timerow['headers']:
                    text = tidal_timerow.getText()

                if text:
                    msg.append(f'{" ".join(text.split())} ')

        if msg:
            return ' '.join(msg)

        return ''
