#!/usr/bin/env python2
# -*- coding: utf8 -*-

import re
import os
from datetime import datetime

class TaeminMemory(object):
    def __init__(self, taemin):
        self.taemin = taemin
        self.offline_messages = {}

    def on_join(self, serv, connection):
        source = connection.user.name
        chan = connection.chan.name

        if source.lower() in self.offline_messages.keys():
            for msg in self.offline_messages[source.lower()]:
                serv.privmsg(chan, msg)
                self.offline_messages[source.lower()] = []

    def on_pubmsg(self, serv, msg):
        chan = msg.chan.name
        source = msg.user.name

        if msg.key == "say":
            m = re.search("^(\S+)\s*(.*)$", msg.value)
            if m:
                nick = m.group(1)
                msg = m.group(2)
                if nick in self.taemin.channels[chan].users():
                    serv.privmsg(chan, nick + ": " + msg)
                else:
                    if not self.offline_messages.get(nick.lower()):
                        self.offline_messages[nick.lower()] = []
                    self.offline_messages[nick.lower()].append(datetime.now().strftime('%H:%M:%S') + " [" + source + "] " + nick + ": " + msg)

            else:
                serv.privmsg(chan, "[Say] Usage : Pseudo + message, ex : !say Taemin Tu es magnifique")

        for user in msg.highlights:
            if re.compile("^.*" + user.name.lower() + ".*$").match(msg.message.lower()):
                if user not in self.taemin.channels[chan].users():
                    if not self.offline_messages.get(user.lower()):
                        self.offline_messages[user.lower()] = []

                    self.offline_messages[user.name.lower()].append(datetime.now().strftime('%H:%M:%S') + " [" + source + "] " + msg.message)


