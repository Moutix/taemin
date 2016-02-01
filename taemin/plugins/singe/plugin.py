#!/usr/bin/env python2
# -*- coding: utf8 -*-

from singe import Singe

class TaeminSinge(object):
    helper = {"singe": "Joue au singe. Usage: !singe lettre"}

    def __init__(self, taemin):
        self.taemin = taemin
        self.singe = Singe()

    def on_pubmsg(self, serv, msg):
        if msg.key != "singe":
            return
        chan = msg.chan.name

        if msg.value == "":
            if self.singe.start_word == "":
                self.singe.play()
            serv.privmsg(chan, "%s" % self.singe.start_word)
            return

        try:
            test = self.singe.add_letter(msg.value)
        except NameError as err:
            test = None
            serv.privmsg(chan, "Nope: %s" % err.message)

        if test:
            if self.singe.play():
                serv.privmsg(chan, "%s" % self.singe.start_word)
                if not self.singe.next_words():
                    serv.privmsg(chan, "J'ai gagné !!! \o/")
                    self.singe.restart()
            else:
                serv.privmsg(chan, "J'ai perdu T.T")
                self.singe.restart()

        elif test is False:
            serv.privmsg(chan, "T'as perdu. :p Je pensais à ça : %s" % self.singe.word())
            self.singe.restart()

