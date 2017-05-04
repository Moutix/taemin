#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin

class TaeminCafe(plugin.TaeminPlugin):
    helper = {"all": "Envoie un message à tout le monde",
              "cafe": "Appelle tout le monde pour prendre un café ;)"}


    def on_pubmsg(self, msg):
        if msg.key not in ("all", 'tous', "cafe"):
            return

        chan = msg.chan.name

        message = " ".join([user.name for user in self.taemin.list_users(msg.chan)])
        if msg.key == "cafe":
            message = "<<< CAFE !!! \\o/ %s \\o/ !!! CAFE >>>" % message
        else:
            message = "%s %s" % (message, msg.value)

        self.privmsg(chan, message)

