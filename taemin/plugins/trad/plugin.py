#!/usr/bin/env python2
# -*- coding: utf8 -*-

from trad import Traduction
from taemin import plugin

class TaeminTrad(plugin.TaeminPlugin):
    helper = {"trad": "Traduit une phrase. Usage: !trad langue1 langue2 mot"}

    def on_pubmsg(self, msg):
        if msg.key != "trad":
            return

        options = self.parse_option(msg.value)

        trad = Traduction.translate(options["word"], options["dst"], options["src"])
        text = "[%s->%s] %s" % (trad.src, trad.dst, trad.word)
        if trad.romaji:
            text += " (%s)" % trad.romaji

        self.privmsg(msg.chan.name, text)

    @staticmethod
    def parse_option(option):
        option = option.split(" ", 2)
        options = {"src": "auto", "dst": "fr"}

        if not option:
            return options

        if len(option) == 1 or option[0] not in Traduction.available_languages():
            options["word"] = " ".join(option)
            return options

        if len(option) == 2 or option[1] not in Traduction.available_languages():
            options["word"] = " ".join(option[1:])
            options["dst"] = option[0]
            return options

        options["word"] = option[2]
        options["src"] = option[0]
        options["dst"] = option[1]
        return options

