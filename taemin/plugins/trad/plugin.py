#!/usr/bin/env python2
# -*- coding: utf8 -*-

from trad import Traduction
from taemin import plugin

class TaeminTrad(plugin.TaeminPlugin):
    helper = {"trad": "Traduit une phrase. Usage: !trad langue1 langue2 mot"}

    def on_pubmsg(self, msg):
        if msg.key != "trad":
            return

        val = msg.value.split(" ", 2)
        if len(val) < 3:
            self.privmsg(msg.chan.name, "Utilisation : !trad langue1 langue2 mot")
        else:
            trad = Traduction(val[2], val[0], val[1])
            text = trad.trad
            if trad.romaji:
                text += " (%s)" % trad.romaji
            self.privmsg(msg.chan.name, text)

