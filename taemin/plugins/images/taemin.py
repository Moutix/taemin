#!/usr/bin/env python2
# -*- coding: utf8 -*-

import re
from image import ImageSearch

class TaeminImage(object):
    MATCH_WORD = "taemin"

    def __init__(self, taemin):
        self.taemin = taemin

    def on_pubmsg(self, serv, canal, message, key, value, **kwargs):
        if key == "donne" or key == "give":
            serv.privmsg(canal, ImageSearch(self.taemin.conf, value).tiny)

        if re.compile("^.*" + self.MATCH_WORD.lower() + ".*$").match(message.lower()):
            serv.privmsg(canal, ImageSearch(self.taemin.conf).tiny)

    def on_privmsg(self, serv, source, key, value, **kwargs):
        if key == "donne" or key == "give":
            serv.privmsg(source, ImageSearch(self.taemin.conf, value).tiny)
        else:
            serv.privmsg(source, ImageSearch(self.taemin.conf).tiny)

