#!/usr/bin/env python2
# -*- coding: utf8 -*-

class TaeminAscii(object):
    def __init__(self, taemin):
        self.taemin = taemin

    def on_pubmsg(self, serv, canal, key, **kwargs):
        if key == "taeminnie":
            serv.privmsg(canal, "  \\o/")
            serv.privmsg(canal, "   |")
            serv.privmsg(canal, "  / \\")

        elif key == "shinee":
            serv.privmsg(canal, " <<<< SHINEE >>>>")
            serv.privmsg(canal, " \\o  o/\\o/\\o  o/")
            serv.privmsg(canal, "  |\\/|  |  |\\/|")
            serv.privmsg(canal, " / \\/ \\/ \\/ \\/ \\")


