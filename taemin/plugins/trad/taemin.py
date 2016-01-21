#!/usr/bin/env python2
# -*- coding: utf8 -*-

from trad import Traduction

class TaeminTrad(object):
    def __init__(self, taemin):
        self.taemin = taemin

    def on_pubmsg(self, serv, canal, message, key, value, **kwargs):
        if key != "trad":
            return

        val = value.split(" ", 2)
        if len(val) < 3:
            serv.privmsg(canal, "Utilisation : !trad langue1 langue2 mot")
        else:
            trad = Traduction(val[2], val[0], val[1])
            text = trad.trad
            if trad.romaji:
                text += " (%s)" % trad.romaji
            serv.privmsg(canal, text)



