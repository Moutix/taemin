#!/usr/bin/env python2
# -*- coding: utf8 -*-

from akinator import Akinator

class TaeminAkinator(object):
    helper = {"akinator": "Qui est-ce: Usage: !akinator [oui|non|sais pas|probablement|probablement pas|restart]"}
    answers = {"oui": 0, "non": 1, "sais pas": 2, "probablement": 3, "probablement pas": 4}

    def __init__(self, taemin):
        self.taemin = taemin
        self.akinators = {}

    def on_pubmsg(self, serv, msg):
        if msg.key != "akinator":
            return

        user = msg.user.name
        chan = msg.chan.name

        if user not in self.akinators or msg.value == "restart":
            self.akinators[user] = Akinator()
            serv.privmsg(chan, "%s" % self.akinators[user].question)
            return

        if msg.value not in self.answers:
            serv.privmsg(chan, self.helper["akinator"])
            serv.privmsg(chan, "%s %s" % (self.print_progression(self.akinators[user].progression), self.akinators[user].question))
            return

        self.akinators[user].answer(self.answers[msg.value])
        if self.akinators[user].question == None:
            self.akinators[user] = Akinator()
            serv.privmsg(chan, "Nouvelle partie :) %s" % self.akinators[user].question)
            return

        if self.akinators[user].progression > 99:
            self.akinators[user].result()
            serv.privmsg(chan, "\o/ %s (%s)" % (self.akinators[user].name, self.akinators[user].description))
            self.akinators[user] = Akinator()
            return

        if self.akinators[user].step > 30:
            self.akinators[user].result()
            serv.privmsg(chan, "Ragequit ^^' je dirais : %s (%s)" % (self.akinators[user].name, self.akinators[user].description))
            self.akinators[user] = Akinator()
            return

        serv.privmsg(chan, "%s %s" % (self.print_progression(self.akinators[user].progression), self.akinators[user].question))

    def print_progression(self, progression):
        if progression < 20:
            return "Ok...'"

        if progression < 50:
            return "Hum..."

        if progression < 80:
            return "Oh !"

        if progression < 100:
            return "Ah !"


