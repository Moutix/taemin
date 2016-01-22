#!/usr/bin/env python2
# -*- coding: utf8 -*-

import re
from image import ImageSearch

class TaeminImage(object):
    def __init__(self, taemin):
        self.taemin = taemin
        self.confapi = self.taemin.conf.get("googleApi", {})
        self.confimage = self.taemin.conf.get("ImageSearch", {})
        self.image = ImageSearch(self.confapi.get("CX"), self.confapi.get("APIKEY"))

    def on_pubmsg(self, serv, canal, message, key, value, **kwargs):
        if key == "donne" or key == "give":
            self.image.search(value)
            serv.privmsg(canal, self.image.tiny)

        for word in self.confimage.keys():
            if re.compile("^.*" + word + ".*$").match(message.lower()):
                self.image.search(self.confimage[word])
                serv.privmsg(canal, self.image.tiny)

    def on_privmsg(self, serv, source, message, key, value, **kwargs):
        if key == "donne" or key == "give":
            self.image.search(value)
            serv.privmsg(source, self.image.tiny)

        for word in self.confimage.keys():
            if re.compile("^.*" + word + ".*$").match(message.lower()):
                self.image.search(self.confimage[word])
                serv.privmsg(source, self.image.tiny)


