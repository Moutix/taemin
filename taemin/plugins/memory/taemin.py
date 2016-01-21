#!/usr/bin/env python2
# -*- coding: utf8 -*-

import re
import os
from datetime import datetime

class TaeminMemory(object):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    USERS_FILE = os.path.join(__location__, "users.save")

    def __init__(self, taemin):
        self.taemin = taemin
        self.users = []
        self.offline_messages = {}

        with open(self.USERS_FILE, 'r') as f:
            for line in f:
                if line != "\n" and line not in self.users:
                    self.users.append(line.replace("\n", ""))

    def on_join(self, serv, source, canal, **kwargs):
        if source.lower() in self.offline_messages.keys():
            for msg in self.offline_messages[source.lower()]:
                serv.privmsg(canal, msg)
                self.offline_messages[source.lower()] = []

        if source != self.taemin.name:
            with open(self.USERS_FILE, 'a') as f:
                for user in self.taemin.channels[canal].users() + [source]:
                    if user not in self.users:
                        self.users.append(user)
                        f.write(user + "\n")

    def on_pubmsg(self, serv, canal, source, message, key, value, **kwargs):
        if key == "say":
            m = re.search("^(\S+)\s*(.*)$", value)
            if m:
                nick = m.group(1)
                msg = m.group(2)
                if nick in self.taemin.channels[canal].users():
                    serv.privmsg(canal, nick + ": " + msg)
                else:
                    if not self.offline_messages.get(nick.lower()):
                        self.offline_messages[nick.lower()] = []
                    self.offline_messages[nick.lower()].append(datetime.now().strftime('%H:%M:%S') + " [" + source + "] " + nick + ": " + msg)

            else:
                serv.privmsg(canal, "[Say] Usage : Pseudo + message, ex : !say Taemin Tu es magnifique")

        for user in self.users:
            if re.compile("^.*" + user.lower() + ".*$").match(message.lower()):
                if user not in self.taemin.channels[canal].users():
                    if not self.offline_messages.get(user.lower()):
                        self.offline_messages[user.lower()] = []

                    self.offline_messages[user.lower()].append(datetime.now().strftime('%H:%M:%S') + " [" + source + "] " + message)


