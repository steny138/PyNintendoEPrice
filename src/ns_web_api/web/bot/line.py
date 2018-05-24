# -*- coding: utf-8 -*-

from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

from basebot import BaseBot, UserProfile

# 64xj+m7bdKgcso0DyhkfwhXDTqPoRzhccBi7/HVFEJaXt+lXi8wZc+33QCMQtllW6h9/sLk2d42RGQmgCnIZPpmzzyDopjUH0GUv82Q5gmJZUfNQ6Khh+1S5elc8QWkbrgTHU8OZ8v71xIeIbkxh+QdB04t89/1O/w1cDnyilFU=

# 80063e1a3a3a1fbd3eb3ce42571cfda1

# U8c4551a39c652dda7d0f95ca8f3b1b1d

class LYCLineBot(BaseBot):

    def __init__(self):
        self.line_bot_api = LineBotApi('64xj+m7bdKgcso0DyhkfwhXDTqPoRzhccBi7/HVFEJaXt+lXi8wZc+33QCMQtllW6h9/sLk2d42RGQmgCnIZPpmzzyDopjUH0GUv82Q5gmJZUfNQ6Khh+1S5elc8QWkbrgTHU8OZ8v71xIeIbkxh+QdB04t89/1O/w1cDnyilFU=')
        self.handler = WebhookHandler('80063e1a3a3a1fbd3eb3ce42571cfda1')
        self.parser =  WebhookParser('80063e1a3a3a1fbd3eb3ce42571cfda1')

    def send_message(self, text, user_id):
        self.line_bot_api.push_message(user_id, TextSendMessage(text=text))

        return "Send"
    
    def reply_message(self, text, body, signature):
        try:
            events = self.parser.parse(body, signature)

            for event in events:
                self.line_bot_api.reply_message(event.reply_token, self.analysis_message(event.message))
            
        except InvalidSignatureError as e:
            return "authorization failed"
        except LineBotApiError as e:
            return e.error.message
        else:
            return "OK"
        
    def user_profile(self, user_id):
        line_profile = self.line_bot_api.get_profile(user_id)
        if not line_profile:
            return None

        profile = UserProfile()
        profile.id = line_profile.user_id
        profile.name = line_profile.display_name
        profile.description = line_profile.status_message
        profile.picture = line_profile.picture_url

        return profile

    def analysis_message(self, message):
        allow_message_type = { "text":self.reply_by_text, "sticker": self.reply_by_sticker } 

        func = allow_message_type.get(message.type, self.reply_default)

        return func(message)


    def reply_by_text(self, message):
        return  TextSendMessage(text=message.text)
    
    def reply_by_sticker(self, message):
        if int(message.package_id) > 4:
            return TextSendMessage(text="中文豪難喔，公蝦聽謀捏。")
        
        return StickerSendMessage(package_id=message.package_id, sticker_id=message.sticker_id)
    
    def reply_default(self, message):
        return TextSendMessage(text="中文豪難喔，公蝦聽謀捏。")

