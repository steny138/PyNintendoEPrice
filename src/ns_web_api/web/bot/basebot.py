# -*- coding: utf-8 -*-


class BaseBot():
    def send_message(self, text):
        raise NotImplementedError
    
    def reply_message(self, text):
        raise NotImplementedError
