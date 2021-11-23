import os
import hmac
import base64
from hashlib import sha1
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

# # todo this segment can be remove
# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

app_id = os.getenv('PTX_API_ID', '')
app_key = os.getenv('PTX_API_KEY', '')

class Auth():

    def __init__(self):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }
