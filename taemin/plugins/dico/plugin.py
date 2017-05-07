#!/usr/bin/env python2
# -*- coding: utf8 -*-

import os
import random

from .dico import Dico
from taemin import plugin

class TaeminDico(plugin.TaeminPlugin):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    DICO = os.path.join(__location__, "dico.txt")
 
    helper = {
        "dico": "Cherche un mot dans le dictionnaire",
        "wotd": "Affiche la description d'un mot random du dico"
    }

    def find_word(self, min_size=6):
        with open(self.DICO, 'r') as content_file:
            content = [w for w in content_file.read().split("\n") if len(w) >= min_size]

        if content:
            word = random.choice(content)
        else:
            word = self.find_word(min_size-1)

        return word

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        if msg.key == "wotd":
            word = self.find_word()
        else:
            word = msg.value

        dico = Dico(word)

        if dico.descriptions:
            self.privmsg(chan, "Definition de %s: (%s) %s" % (dico.word, dico.definition, dico.description))
            return

        self.privmsg(chan, "Connais pas, tu voulais dire %s ?" % dico.suggestion)

if __name__ == "__main__":
    print(TaeminDico(None).find_word())
