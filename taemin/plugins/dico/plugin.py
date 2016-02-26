#!/usr/bin/env python2
# -*- coding: utf8 -*-

from dico import Dico
from taemin import plugin

class TaeminDico(plugin.TaeminPlugin):
    helper = {"dico": "Cherche un mot dans le dictionnaire"}

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name
        dico = Dico(msg.value)

        if dico.descriptions:
            self.privmsg(chan, "Definition de %s: (%s) %s" % (dico.word, dico.definition, dico.description))
            return

        self.privmsg(chan, "Connais pas, tu voulais dire %s ?" % dico.suggestion)

