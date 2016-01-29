#!/usr/bin/env python2
# -*- coding: utf8 -*-

class TaeminCafe(object):
    def __init__(self, taemin):
        self.taemin = taemin

    def on_pubmsg(self, serv, msg):
        if msg.key not in ("all", "cafe"):
            return

        chan = msg.chan.name

        message = " ".join([user.name for user in self.taemin.list_users(msg.chan)])
        if msg.key == "cafe":
            message = "<<< CAFE !!! \\o/ %s \\o/ !!! CAFE >>>" % message
        else:
            message = "%s %s" % (message, msg.value)

        serv.privmsg(chan, message)

