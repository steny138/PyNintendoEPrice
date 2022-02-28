# coding: utf-8

import requests
import json
from .cache import cache

# rate_url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip?date-format"
rate_url = "http://www.apilayer.net/api/live?access_key=4ed7637038e68219154bd351074ea018&format=1"


class CurrencyRate(object):

    def caculate_rate(self, base_currency, target_currency):
        """計算匯率"""
        if not self.origin_currency + target_currency in self.rate_dict:
            return 0

        rate = ""
        if self.origin_currency.lower() == base_currency.lower():
            rate = self.rate_dict[base_currency + target_currency]
        else:
            if not self.origin_currency + base_currency in self.rate_dict:
                return 0

            temp_rate = self.rate_dict[self.origin_currency + base_currency]
            temp_rate = 1/temp_rate

            rate = temp_rate * \
                self.rate_dict[self.origin_currency + target_currency]
        return rate

    @cache.cached(timeout=3600, key_prefix='rate_dict')
    def __get_rate_dict(self):
        print('extract get a rate dictoinary from a url')
        response = requests.get(rate_url)
        return json.loads(response.text)["quotes"]

    def __init__(self):
        self.origin_currency = "USD"
        self.rate_dict = {}
        if not self.rate_dict:
            self.rate_dict = self.__get_rate_dict()


if __name__ == "__main__":
    r = CurrencyRate()
    print("HKD to TWD: %s" % (r.caculate_rate('HKD', 'TWD')))
    print("AUD to TWD: %s" % (r.caculate_rate('AUD', 'TWD')))
    print("GBP to TWD: %s" % (r.caculate_rate('GBP', 'TWD')))
    print("JPY to TWD: %s" % (r.caculate_rate('JPY', 'TWD')))
    print("EUR to TWD: %s" % (r.caculate_rate('EUR', 'TWD')))
    print("USD to TWD: %s" % (r.caculate_rate('USD', 'TWD')))
