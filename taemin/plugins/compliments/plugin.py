#!/usr/bin/env python2
# -*- coding: utf8 -*-

import random

class TaeminCompliments(object):
    def __init__(self, taemin):
        self.taemin = taemin
        self.com_keywords = self.taemin.conf.get("Compliments", {}).get("com_keyword", [])
        self.compliments = self.taemin.conf.get("Compliments", {}).get("compliments", [])

    def on_pubmsg(self, serv, msg):
        if self.iskw(msg.message):
            serv.privmsg(msg.chan.name, random.choice(self.compliments).encode("utf-8"))

    def iskw(self, message):
        for kw in self.com_keywords:
            if kw.lower() in message.lower():
                return True
        return False
