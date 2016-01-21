#!/usr/bin/env python2
# -*- coding: utf8 -*-

from pendu import Pendu

class TaeminPendu(object):
    def __init__(self, taemin):
        self.taemin = taemin
        self.pendu = Pendu()

    def on_pubmsg(self, serv, canal, message, key, value, **kwargs):
        if key != "pendu":
            return

        if value == "":
            serv.privmsg(canal, "%s" % self.pendu.print_word())
        else:
            try:
                test = self.pendu.test(value)
            except NameError as err:
                test = False
                serv.privmsg(canal, "Nope: %s" % err.message)

            if self.pendu.victory:
                serv.privmsg(canal, "Yeah!!! Tu as gagné en seulement %d essais. Le mot était bien %s" % (len(self.pendu.attempt), self.pendu.word))
                self.pendu.new_word()
                serv.privmsg(canal, "Nouveau pendu: %s" % self.pendu.print_word())
            elif test:
                serv.privmsg(canal, "Yep ça marche \o/")
                serv.privmsg(canal, "%s" % self.pendu.print_word())
            elif self.pendu.victory is None:
                serv.privmsg(canal, "Nope, pas de %s" % value)
                for line in self.pendu.pretty_print().split("\n"):
                    serv.privmsg(canal, "%s" % line)
            else:
                serv.privmsg(canal, "Tu as perdu :(. Le mot était \"%s\"" % self.pendu.word)
                for line in self.pendu.pretty_print().split("\n"):
                    serv.privmsg(canal, "%s" % line)
                self.pendu.new_word()
                serv.privmsg(canal, "Nouveau pendu: %s" % self.pendu.print_word())

    def on_privmsg(self, serv, target, key, value, **kwargs):
        if key != "pendu":
            return

        self.pendu.new_word(0, value)
        for chan in self.taemin.chans:
            serv.privmsg(chan, "Nouveau pendu: %s" % self.pendu.print_word())



