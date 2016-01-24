#!/usr/bin/env python2
# -*- coding: utf8 -*-

from pendu import Pendu

class TaeminPendu(object):
    def __init__(self, taemin):
        self.taemin = taemin
        self.pendu = Pendu()

    def on_pubmsg(self, serv, msg):
        if msg.key != "pendu":
            return

        chan = msg.chan.name

        if msg.value == "":
            serv.privmsg(chan, "%s" % self.pendu.print_word())
        else:
            try:
                test = self.pendu.test(msg.value)
            except NameError as err:
                test = False
                serv.privmsg(chan, "Nope: %s" % err.message)

            if self.pendu.victory:
                serv.privmsg(chan, "Yeah!!! Tu as gagné en seulement %d essais. Le mot était bien %s" % (len(self.pendu.attempt), self.pendu.word))
                self.pendu.new_word()
                serv.privmsg(chan, "Nouveau pendu: %s" % self.pendu.print_word())
            elif test:
                serv.privmsg(chan, "Yep ça marche \o/")
                serv.privmsg(chan, "%s" % self.pendu.print_word())
            elif self.pendu.victory is None:
                serv.privmsg(chan, "Nope, pas de %s" % msg.value)
                for line in self.pendu.pretty_print().split("\n"):
                    serv.privmsg(chan, "%s" % line)
            else:
                serv.privmsg(chan, "Tu as perdu :(. Le mot était \"%s\"" % self.pendu.word)
                for line in self.pendu.pretty_print().split("\n"):
                    serv.privmsg(chan, "%s" % line)
                self.pendu.new_word()
                serv.privmsg(chan, "Nouveau pendu: %s" % self.pendu.print_word())

    def on_privmsg(self, serv, msg):
        if msg.key != "pendu":
            return

        self.pendu.new_word(0, msg.value)
        for chan in msg.user.chans:
            serv.privmsg(chan.name, "Nouveau pendu: %s" % self.pendu.print_word())

