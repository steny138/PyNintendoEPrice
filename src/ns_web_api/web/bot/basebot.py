# -*- coding: utf-8 -*-

class BaseBot():
    def send_message(self, text):
        raise NotImplementedError

    def reply_message(self, text):
        raise NotImplementedError


class UserProfile():
    def __init__(self):
        self.id = ""
        self.name = ""
        self.picture = ""
        self.description = ""
