#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin
from .synonymes import Synonymes

class TaeminSynonymes(plugin.TaeminPlugin):
    helper = {"synonymes": "Cherche les synonymes d'un mot"}

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        synonymes = Synonymes.off(msg.value)

        if synonymes:
            self.privmsg(chan, "Synonymes de %s: %s" % (msg.value, ", ".join(synonymes)))
            return

        self.privmsg(chan, "Pas trouvé de synonymes...")
