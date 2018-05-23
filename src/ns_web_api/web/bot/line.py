# -*- coding: utf-8 -*-

from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from basebot import BaseBot

# 64xj+m7bdKgcso0DyhkfwhXDTqPoRzhccBi7/HVFEJaXt+lXi8wZc+33QCMQtllW6h9/sLk2d42RGQmgCnIZPpmzzyDopjUH0GUv82Q5gmJZUfNQ6Khh+1S5elc8QWkbrgTHU8OZ8v71xIeIbkxh+QdB04t89/1O/w1cDnyilFU=

# 80063e1a3a3a1fbd3eb3ce42571cfda1

# U8c4551a39c652dda7d0f95ca8f3b1b1d

class LYCLineBot(BaseBot):

    def __init__(self):
        self.line_bot_api = LineBotApi('64xj+m7bdKgcso0DyhkfwhXDTqPoRzhccBi7/HVFEJaXt+lXi8wZc+33QCMQtllW6h9/sLk2d42RGQmgCnIZPpmzzyDopjUH0GUv82Q5gmJZUfNQ6Khh+1S5elc8QWkbrgTHU8OZ8v71xIeIbkxh+QdB04t89/1O/w1cDnyilFU=')
        self.handler = WebhookHandler('80063e1a3a3a1fbd3eb3ce42571cfda1')
        self.parser =  WebhookParser('80063e1a3a3a1fbd3eb3ce42571cfda1')

    def send_message(self, text):
        self.line_bot_api.push_message('U8c4551a39c652dda7d0f95ca8f3b1b1d', TextSendMessage(text=text))
    
    def reply_message(self, text, body, signature):
        events = self.parser.parse(body, signature)

        for event in events:
            reply_text = event.message.text
            if text :
                reply_text = text

            self.line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
