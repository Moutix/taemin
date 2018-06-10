"""Petite schnaffon plugin"""

import re

from taemin import plugin

class TaeminPetite(plugin.TaeminPlugin):
    def on_pubmsg(self, msg):

        if not "schnaffon" in msg.message.lower():
            return

        if re.search(r"[p|ℙ]etite\s+schnaffon", msg.message.lower()):
            return

        self.privmsg(msg.chan.name, "-> Petite Schnaffon")
