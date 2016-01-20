#!/usr/bin/env python2
# -*- coding: utf8 -*-

from plugins.trans.trans import Transliterate

class TaeminTrans(object):
    def __init__(self, taemin):
        self.taemin = taemin

    def on_pubmsg(self, serv, canal, message, key, value, **kwargs):
        if key != "trans":
            return

        val = value.split(" ", 1)
        if len(val) < 2:
            serv.privmsg(canal, "Utilisation : !trans alphabet mot")
        else:
            serv.privmsg(canal, Transliterate(val[1], val[0]).trans)

