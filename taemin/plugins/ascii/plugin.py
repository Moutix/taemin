#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin

class TaeminAscii(plugin.TaeminPlugin):
    helper = {"taeminnie": "M'affiche dans ma plus belle forme <3",
              "shinee": "Affiche le groupe le plus joli du monde"}

    def on_pubmsg(self, msg):
        chan = msg.chan.name

        if msg.key == "taeminnie":
            self.privmsg(chan, "  \\o/")
            self.privmsg(chan, "   |")
            self.privmsg(chan, "  / \\")

        elif msg.key == "shinee":
            self.privmsg(chan, " <<<< SHINEE >>>>")
            self.privmsg(chan, " \\o  o/\\o/\\o  o/")
            self.privmsg(chan, "  |\\/|  |  |\\/|")
            self.privmsg(chan, " / \\/ \\/ \\/ \\/ \\")
