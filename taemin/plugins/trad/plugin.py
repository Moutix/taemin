#!/usr/bin/env python2
# -*- coding: utf8 -*-

from trad import Traduction

class TaeminTrad(object):
    def __init__(self, taemin):
        self.taemin = taemin

    def on_pubmsg(self, serv, msg):
        if msg.key != "trad":
            return

        val = msg.value.split(" ", 2)
        if len(val) < 3:
            serv.privmsg(msg.chan.name, "Utilisation : !trad langue1 langue2 mot")
        else:
            trad = Traduction(val[2], val[0], val[1])
            text = trad.trad
            if trad.romaji:
                text += " (%s)" % trad.romaji
            serv.privmsg(msg.chan.name, text)

