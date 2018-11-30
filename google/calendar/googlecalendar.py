# -*- coding: UTF-8 -*-
"""
Shows basic usage of the Google Calendar API. Creates a Google Calendar API
service object and outputs a list of the next 10 events on the user's calendar.
"""
import sys
sys.path.append('./')

import os
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, tools, client
import datetime

credential_path = os.path.join('./google/calendar/credential.json')

# Setup the Calendar API
class Daan(object):

    def __init__(self, id, client_id, client_secret, redirect_uris):
        self.store = file.Storage(credential_path)
        self.id = id
        self.creds = self.store.get()
        if not self.creds or self.creds.invalid:
            self.flow = client.OAuth2WebServerFlow(
             client_id=client_id,
             client_secret=client_secret,
             scope='https://www.googleapis.com/auth/calendar.readonly',
             redirect_uris=redirect_uris)
            self.creds = tools.run_flow(self.flow, self.store)
        self.service = build('calendar', 'v3', http=self.creds.authorize(Http()))

# Call the Calendar API
    def getschedule(self,name):
        data ='' 
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = self.service.events().list(calendarId=self.id, timeMin=now,singleEvents=True,q=name, fields='items').execute()
        events = events_result.get('items', [])
        
        if not events:
            return ''
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            data = data + ' ' + start + ' ' + event['summary'] + '\n'
        return name + ' 本月排班:\n' + data[:-1]
