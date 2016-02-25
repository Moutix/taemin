#!/usr/bin/env python2
# -*- coding: utf8 -*-

from dico import Dico

class TaeminDico(object):
    helper = {"dico": "Cherche un mot dans le dictionnaire"}
    def __init__(self, taemin):
        self.taemin = taemin

    def on_pubmsg(self, serv, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name
        dico = Dico(msg.value)

        if dico.descriptions:
            serv.privmsg(chan, "Definition de %s: (%s) %s" % (dico.word, dico.definition, dico.description))
            return

        serv.privmsg(chan, "Connais pas, tu voulais dire %s ?" % dico.suggestion)

