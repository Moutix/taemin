#!/usr/bin/env python2
# -*- coding: utf8 -*-

from trans import Transliterate
from taemin import plugin

class TaeminTrans(plugin.TaeminPlugin):
    helper = {"trans": "Translitère dans un autre alphabet. Usage: !trans alphabet mot"}

    def on_pubmsg(self, msg):
        if msg.key != "trans":
            return

        val = msg.value.split(" ", 1)
        if len(val) < 2:
            self.privmsg(msg.chan.name, "Utilisation : !trans alphabet mot")
        else:
            self.privmsg(msg.chan.name, Transliterate(val[1], val[0]).trans)

