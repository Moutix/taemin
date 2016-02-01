#!/usr/bin/env python2
# -*- coding: utf8 -*-

import re
from image import ImageSearch
from taemin import env

class TaeminImage(object):
    helper = {"donne": "Recherche sur google image",
              "give": "Recherche sur google image"}

    def __init__(self, taemin):
        self.taemin = taemin
        self.confapi = env.conf.get("googleApi", {})
        self.confimage = env.conf.get("ImageSearch", {})
        self.image = ImageSearch(self.confapi.get("CX"), self.confapi.get("APIKEY"))

    def on_pubmsg(self, serv, msg):
        chan = msg.chan.name

        if msg.key == "donne" or msg.key == "give":
            self.image.search(msg.value)
            serv.privmsg(chan, self.image.tiny)

        for word in self.confimage.keys():
            if re.compile("^.*" + word + ".*$").match(msg.message.lower()):
                self.image.search(self.confimage[word])
                serv.privmsg(chan, self.image.tiny)

    def on_privmsg(self, serv, msg):
        source = msg.user.name

        if msg.key == "donne" or msg.key == "give":
            self.image.search(msg.value)
            serv.privmsg(source, self.image.tiny)

        for word in self.confimage.keys():
            if re.compile("^.*" + word + ".*$").match(msg.message.lower()):
                self.image.search(self.confimage[word])
                serv.privmsg(source, self.image.tiny)


def main():
    print TaeminImage().image

if __name__ == "__name__":
    main()


