# -*- coding: utf-8 -*-

# Use google/google-api-python-client to storage data into google sheet
# We Save the All of games which nintendo games and these game tw name.

from __future__ import print_function
import os
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.service_account import ServiceAccountCredentials
from ns_web_crawler import settings

class GoogleSheetApiPipeline(object):
    def open_spider(self, spider):
        # Setup the Sheets API
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
        cred_file_path = os.path.join(APP_ROOT, 'client_secret.json')
        creds = ServiceAccountCredentials.from_json_keyfile_name(cred_file_path, SCOPES)
        
        if not creds or creds.invalid:
            raise Exception('No Credentials')
        self.service = build('sheets', 'v4', http=creds.authorize(Http()))


    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):

        # Call the Sheets API
        SPREADSHEET_ID = settings.SPREADSHEET
        RANGE_NAME = 'Games!A2:E'
        result = self.service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                    range=RANGE_NAME).execute()

        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            print('Name, Major:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('%s, %s' % (row[0], row[4]))
        return item

if __name__ == "__main__":
    pipline = GoogleSheetApiPipeline()
    pipline.process_item(None, None)