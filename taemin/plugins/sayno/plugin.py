#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin

class TaeminSayNo(plugin.TaeminPlugin):
    def __init__(self, taemin):
        plugin.TaeminPlugin.__init__(self, taemin)
        self.non_keyword = self.taemin.conf.get("SayNo", {}).get("non_keyword", [])
        self.non_nick = self.taemin.conf.get("SayNo", {}).get("non_nick", [])

    def on_pubmsg(self, msg):
        if self._say_no(msg.message):
            self.privmsg(msg.chan.name, "NON")

    def _say_no(self, message):
        test = False
        for nick in self.non_nick:
            if nick.lower() in message.lower():
                test |= True
        if not test:
            return False

        test = False
        for key in self.non_keyword:
            test |= key in message

        return test


