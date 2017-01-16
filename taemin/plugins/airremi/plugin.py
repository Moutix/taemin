#!/usr/bin/env python2
# -*- coding: utf8 -*-

import random
import os

from taemin import plugin

class TaeminAirremi(plugin.TaeminPlugin):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    DICO_FILE = (os.path.join(__location__, "dico.txt"))
    with open(DICO_FILE, 'r') as content_file:
        DICO = content_file.read().split("\n")

    helper = {}

    def on_pubmsg(self, msg):
        if " " in msg.message.strip():
            return

        word = self.find_word(msg.message)
        if not word:
            return

        self.privmsg(msg.chan.name, word)

    @classmethod
    def find_word(cls, prefix):
        available_words = [w for w in cls.DICO if len(w) > len(prefix) and w[:len(prefix)].lower() == prefix.lower()]
        if not available_words:
            return None

        return random.choice(available_words)[len(prefix):]
