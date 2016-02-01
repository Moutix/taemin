#!/usr/bin/env python2
# -*- coding: utf8 -*-

import re
import os
from datetime import datetime

class TaeminMemory(object):
    helper = {"say": "Me fait dire quelque chose à quelqu'un"}

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
                val = m.group(2)
                if nick.lower() in [user.lower() for user in self.taemin.list_user_name(chan)]:
                    serv.privmsg(chan, nick + ": " + val)
                else:
                    if not self.offline_messages.get(nick.lower()):
                        self.offline_messages[nick.lower()] = []
                    self.offline_messages[nick.lower()].append(datetime.now().strftime('%H:%M:%S') + " [" + source + "] " + nick + ": " + val)

            else:
                serv.privmsg(chan, "[Say] Usage : Pseudo + message, ex : !say Taemin Tu es magnifique")

        for user in msg.highlights:
            if not user.online:
                if not self.offline_messages.get(user.name.lower()):
                    self.offline_messages[user.name.lower()] = []

                self.offline_messages[user.name.lower()].append(datetime.now().strftime('%H:%M:%S') + " [" + source + "] " + msg.message)


