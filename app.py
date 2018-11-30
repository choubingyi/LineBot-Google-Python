#!/usr/bin/env python3  
# -*- coding: utf-8 -*-  
import sys
sys.path.append('./google/calendar')
sys.path.append('./google')

import googlecalendar

import os
import requests
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselTemplate, MessageAction, CarouselColumn, PostbackEvent, PostbackAction
)

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
SECRET = os.environ.get('SECRET')
CALENDAR_ID = os.environ.get('calendarID')
client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
redirect_uris = os.environ.get('redirect_uris')

TEAM_NAME = os.environ.get('TEAM_NAME')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    #print(body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    res = event.message.text
    if check_event_message(res) ==1:
        send_search_list(event)
    else:
        return 'do nothing.'

@handler.add(PostbackEvent)
def handle_postevent(event):
    res = event.postback.data
    if res in TEAM_NAME:
        send_calendar_schedule(event)    

def check_event_message(message):
    return {
            'search' : 'show function',
            '查詢' : 1,
            '節氣' : '節氣'
    }.get(message,'keyword not found')

def send_search_list(event):
    columns = []
    for name_list in eval(TEAM_NAME):
        action_list = [PostbackAction(label=name.strip(), data=name.strip()) for name in name_list]
        columns.append(CarouselColumn(
            thumbnail_image_url = 'https://www.wabion.com/wp-content/uploads/2018/07/google_cloud_search_512dp.png',
            title = 'select your name',
            text = ' ',
            actions = action_list))
       
    message = TemplateSendMessage(alt_text = 'Check your work date.',
                                template = CarouselTemplate(columns = columns))
    line_bot_api.reply_message(event.reply_token, message)

def send_calendar_schedule(event):
    calendar = googlecalendar.Daan(CALENDAR_ID, client_id, client_secret, redirect_uris)
    schedule = calendar.getschedule(event.postback.data)
    if schedule != '':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=schedule))
               
if __name__ == "__main__":
    app.run()
