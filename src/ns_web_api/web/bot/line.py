# -*- coding: utf-8 -*-

from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage,
    TemplateSendMessage,
    Template,
    ButtonsTemplate,
    ConfirmTemplate,
    CarouselTemplate,
    CarouselColumn,
    TemplateAction,
    PostbackTemplateAction,
    MessageTemplateAction,
    URITemplateAction,
    DatetimePickerTemplateAction,
    ImageCarouselTemplate,
    ImageCarouselColumn
)

import jieba

from .basebot import BaseBot, UserProfile

from events.analyzer import analyzer

import logging

logger = logging.getLogger('flask.app')


class LYCLineBot(BaseBot):

    def __init__(self, access_token, secret):
        self.line_bot_api = LineBotApi(access_token)
        self.handler = WebhookHandler(secret)
        self.parser = WebhookParser(secret)

    def send_message(self, text, user_id):
        self.line_bot_api.push_message(user_id, TextSendMessage(text=text))

        return "send"

    def boardcast(self, text):
        self.line_bot_api.broadcast(TextSendMessage(text=text))

        return "broadcast"

    def reply_message(self, text, body, signature):
        try:
            events = self.parser.parse(body, signature)

            for event in events:
                return_message = self.special_reply(event.message)

                # 沒有特殊處理過的回應, 解析一下訊息在處理回應
                if not return_message:
                    return_message = self.analysis_message(event.message)

                self.line_bot_api.reply_message(
                    event.reply_token, return_message)

        except InvalidSignatureError as e:
            return f"authorization failed: {e.error.message}"
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
        """解析使用者傳的訊息來決定回傳什麼東西給使用者

        Arguments:
            message {[MessageEvent.Message]} -- [the message event from user pass]

        Returns:
            [SendMessage] -- [the message what postback to the user.]
        """

        # 解析是不是有符合觸發事件
        if message.type == "text":
            seg_list = ", ".join(jieba.cut(message.text)).split(', ')
            logger.info(f'vocabulary {seg_list}')
            match_event_message = analyzer.match(seg_list)
            match_event_message = list(
                filter(lambda x: x is not None, match_event_message))
            if match_event_message and len(match_event_message) > 0:
                print(f'match event {match_event_message}')
                return TextSendMessage(text=''.join(filter(lambda x: x is not None, match_event_message)))

        # 沒有就去當鸚鵡吧
        allow_message_type = {"text": self.reply_by_text,
                              "sticker": self.reply_by_sticker}

        func = allow_message_type.get(message.type, self.reply_default)
        return func(message)

    def reply_by_text(self, message):
        """reply a text

        Arguments:
            message {string} -- request message

        Returns:
            string -- response message
        """

        return TextSendMessage(text=message.text)

    def reply_by_sticker(self, message):
        """reply by a sticker

        Arguments:
            message {string} -- request message

        Returns:
            string  -- response sticker.
        """

        if int(message.package_id) > 4:
            return TextSendMessage(text="中文豪難喔，公蝦聽謀捏。")

        return StickerSendMessage(package_id=message.package_id, sticker_id=message.sticker_id)

    def reply_default(self, message):
        return TextSendMessage(text="中文豪難喔，公蝦聽謀捏。")

    def template_buttons(self, message):
        """produce template with buttons

        Arguments:
            message {[MessageEvent.Message]} -- [the message event from user pass]
        """
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/ZgVAAMV.jpg',
                title='LYC電玩展',
                text='您今天想看什麼任天堂Switch遊戲',
                actions=[
                    PostbackTemplateAction(
                        label='最新的',
                        text='最新的',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='特價中的',
                        text='特價中的'
                    ),
                    URITemplateAction(
                        label='我自己看吧',
                        uri='https://lycnsbot.herokuapp.com/games'
                    )
                ]
            )
        )
        return buttons_template_message

    def template_confirm(self, message):
        """produce template with confirm button

        Arguments:
            message {[MessageEvent.Message]} -- [the message event from user pass]
        """
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='你準備好買更多的任天堂了嗎?',
                actions=[
                    PostbackTemplateAction(
                        label='當然啊',
                        text='我要買任天堂Switch',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='不買行嗎',
                        text='我不買任天堂Switch'
                    )
                ]
            )
        )
        return confirm_template_message

    def template_carousel_buttons(self, message):
        """produce template with carousel buttons

        Arguments:
            message {[MessageEvent.Message]} -- [the message event from user pass]
        """
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/njZeeBz.jpg',
                        title='Splatoon 2',
                        text='花枝會打漆彈耶',
                        actions=[
                            MessageTemplateAction(
                                label='哇嗚好像很好玩',
                                text='真的不錯玩'
                            ),
                            MessageTemplateAction(
                                label='我覺得不行',
                                text='你不行？ 你身上哪裡不行'
                            ),
                            URITemplateAction(
                                label='現在價錢如何',
                                uri='https://eshop-prices.com/games/260-splatoon-2'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/p3ozN9s.jpg',
                        title='The Legend Of Zelda-Breath Of The Wild',
                        text='薩爾達傳說之精神時光屋',
                        actions=[
                            MessageTemplateAction(
                                label='哇嗚好像很好玩',
                                text='真的不錯玩'
                            ),
                            MessageTemplateAction(
                                label='我覺得不行',
                                text='你不行？ 你身上哪裡不行'
                            ),
                            URITemplateAction(
                                label='現在價錢如何',
                                uri='https://eshop-prices.com/games/378-the-legend-of-zelda-breath-of-the-wild'
                            )
                        ]
                    )
                ]
            )
        )
        return carousel_template_message

    def template_carousel_images(self, message):
        """produce template with carousel images

        Arguments:
            message {[MessageEvent.Message]} -- [the message event from user pass]
        """
        image_carousel_template_message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/njZeeBz.jpg',
                        action=PostbackTemplateAction(
                            label='Splatoon 2 漆彈大作戰',
                            text='快來打漆彈',
                            data='action=buy&itemid=1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/p3ozN9s.jpg',
                        action=PostbackTemplateAction(
                            label='薩爾達傳說之精神時光屋',
                            text='人馬？ 給虐嗎?',
                            data='action=buy&itemid=2'
                        )
                    )
                ]
            )
        )

        return image_carousel_template_message

    def special_reply(self, message):
        """特殊處理的回覆訊息

        Arguments:
            message {[MessageEvent.Message]} -- [the message event from user pass]

        Returns:
            [SendMessage] -- [the special message what postback to the user.]
        """

        match_stickers = {
            "1-10": self.template_buttons,
            "1-2": self.template_confirm,
            "1-4": self.template_carousel_buttons,
            "1-13": self.template_carousel_images
        }
        if message.type == "sticker":
            key = "{0}-{1}".format(message.package_id, message.sticker_id)
            func = match_stickers.get(key, lambda s: None)

            return func(message)

        return None
