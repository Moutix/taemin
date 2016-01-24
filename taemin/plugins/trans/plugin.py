#!/usr/bin/env python2
# -*- coding: utf8 -*-

from trans import Transliterate

class TaeminTrans(object):
    def __init__(self, taemin):
        self.taemin = taemin

    def on_pubmsg(self, serv, msg):
        if msg.key != "trans":
            return

        val = msg.value.split(" ", 1)
        if len(val) < 2:
            serv.privmsg(msg.chan.name, "Utilisation : !trans alphabet mot")
        else:
            serv.privmsg(msg.chan.name, Transliterate(val[1], val[0]).trans)

