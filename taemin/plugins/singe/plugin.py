#!/usr/bin/env python2
# -*- coding: utf8 -*-

from singe import Singe
from taemin import plugin

class TaeminSinge(plugin.TaeminPlugin):
    helper = {"singe": "Joue au singe. Usage: !singe lettre"}

    def __init__(self, taemin):
        plugin.TaeminPlugin.__init__(self, taemin)
        self.singe = Singe()

    def on_pubmsg(self, msg):
        if msg.key != "singe":
            return
        chan = msg.chan.name

        if msg.value == "":
            if self.singe.start_word == "":
                self.singe.play()
            self.privmsg(chan, "%s" % self.singe.start_word)
            return

        try:
            test = self.singe.add_letter(msg.value)
        except NameError as err:
            test = None
            self.privmsg(chan, "Nope: %s" % err.message)

        if test:
            if self.singe.play():
                self.privmsg(chan, "%s" % self.singe.start_word)
                if not self.singe.next_words():
                    self.privmsg(chan, "J'ai gagné !!! \o/")
                    self.singe.restart()
            else:
                self.privmsg(chan, "J'ai perdu T.T")
                self.singe.restart()

        elif test is False:
            self.privmsg(chan, "T'as perdu. :p Je pensais à ça : %s" % self.singe.word())
            self.singe.restart()

