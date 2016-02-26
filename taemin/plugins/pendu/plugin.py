#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin
from pendu import Pendu

class TaeminPendu(plugin.TaeminPlugin):
    helper = {"pendu": "Joue au pendu"}

    def __init__(self, taemin):
        plugin.TaeminPlugin.__init__(self, taemin)
        self.pendu = Pendu()

    def on_pubmsg(self, msg):
        if msg.key != "pendu":
            return

        chan = msg.chan.name

        if msg.value == "":
            self.privmsg(chan, "%s" % self.pendu.print_word())
        else:
            try:
                test = self.pendu.test(msg.value)
            except NameError as err:
                test = False
                self.privmsg(chan, "Nope: %s" % err.message)

            if self.pendu.victory:
                self.privmsg(chan, "Yeah!!! Tu as gagné en seulement %d essais. Le mot était bien %s" % (len(self.pendu.attempt), self.pendu.word))
                self.pendu.new_word()
                self.privmsg(chan, "Nouveau pendu: %s" % self.pendu.print_word())
            elif test:
                self.privmsg(chan, "Yep ça marche \o/")
                self.privmsg(chan, "%s" % self.pendu.print_word())
            elif self.pendu.victory is None:
                self.privmsg(chan, "Nope, pas de %s" % msg.value)
                for line in self.pendu.pretty_print().split("\n"):
                    self.privmsg(chan, "%s" % line)
            else:
                self.privmsg(chan, "Tu as perdu :(. Le mot était \"%s\"" % self.pendu.word)
                for line in self.pendu.pretty_print().split("\n"):
                    self.privmsg(chan, "%s" % line)
                self.pendu.new_word()
                self.privmsg(chan, "Nouveau pendu: %s" % self.pendu.print_word())

    def on_privmsg(self, msg):
        if msg.key != "pendu":
            return

        self.pendu.new_word(0, msg.value)
        for connection in msg.user.connections:
            self.privmsg(connection.chan.name, "Nouveau pendu: %s" % self.pendu.print_word())

