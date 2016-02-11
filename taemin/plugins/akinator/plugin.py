#!/usr/bin/env python2
# -*- coding: utf8 -*-

from akinator import Akinator, AkinatorError

class TaeminAkinator(object):
    helper = {"akinator": "Qui est-ce: Usage: !akinator [oui|non|sais pas|probablement|probablement pas|restart]"}
    answers = {"oui": 0, "non": 1, "sais pas": 2, "probablement": 3, "probablement pas": 4}
    expressions = [(20, "Ok..."), (50, "Hum..."), (80, "Oh !"), (100, "Ah !")]

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

        try:
            self.akinators[user].answer(self.answers[msg.value])
        except AkinatorError:
            self.akinators[user] = Akinator()
            serv.privmsg(chan, "Nouvelle partie :) %s" % self.akinators[user].question)
            return

        if self.akinators[user].progression > 99:
            self.akinators[user].result()
            serv.privmsg(chan, "\o/ %s (%s) %s" % (self.akinators[user].name, self.akinators[user].description, self.akinators[user].image))
            self.akinators[user] = Akinator()
            return

        if self.akinators[user].step in (30, 50, 70, 100):
            self.akinators[user].result()
            serv.privmsg(chan, "Ragequit ^^' je dirais : %s (%s) %s" % (self.akinators[user].name, self.akinators[user].description, self.akinators[user].image))

            if self.akinators[user].step == 100:
                self.akinators[user] = Akinator()
                return

        serv.privmsg(chan, "%s %s" % (self.print_progression(self.akinators[user].progression), self.akinators[user].question))

    def print_progression(self, progression):
        for value, expression in self.expressions:
            if progression <= value:
                return expression
        return "..."

