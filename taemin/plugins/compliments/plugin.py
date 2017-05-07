#!/usr/bin/env python2
# -*- coding: utf8 -*-

import random
from taemin import plugin

class TaeminCompliments(plugin.TaeminPlugin):
    def __init__(self, taemin):
        plugin.TaeminPlugin.__init__(self, taemin)
        self.com_keywords = self.taemin.conf.get("Compliments", {}).get("com_keyword", [])
        self.compliments = self.taemin.conf.get("Compliments", {}).get("compliments", [])

    def on_pubmsg(self, msg):
        if self.iskw(msg.message):
            self.privmsg(msg.chan.name, random.choice(self.compliments))

    def iskw(self, message):
        for kw in self.com_keywords:
            if kw.lower() in message.lower():
                return True
        return False
