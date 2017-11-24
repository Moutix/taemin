#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin

class TaeminPiou(plugin.TaeminPlugin):
    helper = {}

    def on_pubmsg(self, msg):
        if msg.message.strip() == "bn":
            self.privmsg(msg.chan.name, "bn")
