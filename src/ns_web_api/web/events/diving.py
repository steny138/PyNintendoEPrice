import requests
import logging

from bs4 import BeautifulSoup

logger = logging.getLogger('flask.app')

class DivingEvent(object):
    """ 潛水事件
    """

    def __init__(self):
        self.diving_place = [
            '小琉球',
            '墾丁',
            '後壁湖',
            '綠島',
            '蘭嶼',
            '東北角'
        ]

    def occurs(self, vocabulary):
        """潛水事件觸發
        """
        if not vocabulary:
            return

        return_msg = []
        
        logger.info(f'潛點事件處理: {vocabulary}')

        if all(elem in self.diving_place for elem in vocabulary):
            for v in vocabulary:
                return_msg.append(self.__diving_event(v))
        
        return ', '.join(return_msg)

    def __diving_event(self, vocabulary):
        """潛點事件處理
        """

        sea_id_dict = {
            '小琉球': 'OSea07',
            '綠島': 'OSea10',
            '蘭嶼': 'OSea10',
            '墾丁': 'OSea08',
            '後壁湖': 'OSea08',
            '東北角': 'OSea01'
        }        

        sea_id = sea_id_dict.get(vocabulary, 'index')

        url = f'https://www.cwb.gov.tw/V8/C/M/OBS_Marine/48hrsSeaObs_MOD/{sea_id}.html'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        rows = soup.select('tr')

        msg = []
        for row in rows:
            title = row.select_one('th a').getText()
            title = " ".join(title.split())
            
            if vocabulary not in title:
                continue

            wind = row.select('td')[5].select_one('span.wind span.sr-only')
            wind_txt = wind.getText() if wind is not None else ''

            temperature = row.select('td')[7].select_one('span.tempC')
            temperature_txt = temperature.getText() if temperature is not None else ''

            if temperature_txt and temperature_txt != '-':
                msg.append(f'{" ".join(title.split())}' + \
                f' 風向{" ".join(wind_txt.split())}' + \
                f' 海溫{" ".join(temperature_txt.split())}度')

        if msg:
            return ' '.join(msg)
        
        return f'{vocabulary}查無海流資訊'


