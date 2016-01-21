#!/usr/bin/env python2
# -*- coding: utf8 -*-

from singe import Singe

class TaeminSinge(object):
    def __init__(self, taemin):
        self.taemin = taemin
        self.singe = Singe()

    def on_pubmsg(self, serv, canal, message, key, value, **kwargs):
        if key != "singe":
            return

        if value == "":
            if self.singe.start_word == "":
                self.singe.play()
            serv.privmsg(canal, "%s" % self.singe.start_word)
        else:
            try:
                test = self.singe.add_letter(value)
            except NameError as err:
                test = None
                serv.privmsg(canal, "Nope: %s" % err.message)

            if test:
                if self.singe.play():
                    serv.privmsg(canal, "%s" % self.singe.start_word)
                    if not self.singe.next_words():
                        serv.privmsg(canal, "J'ai gagné !!! \o/")
                        self.singe.restart()
                else:
                    serv.privmsg(canal, "J'ai perdu T.T")
                    self.singe.restart()
            elif test is False:
                serv.privmsg(canal, "T'as perdu. :p Je pensais à ça : %s" % self.singe.word())
                self.singe.restart()

    def on_privmsg(self, serv, target, key, value, **kwargs):
        pass



