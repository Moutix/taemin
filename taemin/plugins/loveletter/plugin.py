#!/usr/bin/env python2
# -*- coding: utf8 -*-

from loveletter import LoveLetter

class TaeminLoveLetter(object):
    helper = {"loveletter": "Joue à loveletter. Usage: !loveletter start|join|restart|play"}

    def __init__(self, taemin):
        self.taemin = taemin
        self.loveletter = LoveLetter()

    def on_pubmsg(self, serv, msg):
        if msg.key != "loveletter":
            return

        chan = msg.chan.name
        value = msg.value
        source = msg.user.name


        if value == "":
            serv.privmsg(chan, "start pour commencer la partie, restart pour la recommencer")
        elif value == "start":
            try:
                self.loveletter.start()
            except ValueError as err:
                serv.privmsg(chan, "%s, join pour rejoindre la partie" % err.message)
            for player in self.loveletter.turn:
                serv.privmsg(player.name, "Tes cartes : %s" % player.cards)
                serv.privmsg(player.name, "Pour jouer dans le chan : !loveletter play carte_à_jouer personne_visée carte_visée")

        elif value == "restart":
            self.loveletter.restart()
        elif value == "join":
            try:
                self.loveletter.add_player(source)
            except NameError as err:
                serv.privmsg(chan, err.message)
        elif value[:4] == "play":
            options = value.split(" ")
            card = ""
            target_player = None
            target_card = None
            if len(options) >= 2:
                card = options[1]
                if len(options) >= 3:
                    target_player = options[2]
                    if len(options) >= 4:
                        target_card = options[3]
                try:
                    result = self.loveletter.play(source, card, target_player, target_card)
                except (NameError, ValueError) as err:
                    result = err.message
                if result[:4] == "PRIV":
                    serv.privmsg(source, "%s" % result[5:])
                else:
                    serv.privmsg(chan, result)
                for player in self.loveletter.turn:
                    serv.privmsg(player.name, "Tes cartes : %s" % player.cards)

                if self.loveletter.find_winner():
                    serv.privmsg(chan, "%s a gagné !!!" % self.loveletter.find_winner().name)
                    self.loveletter.restart()
            else:
                serv.privmsg(chan, "Utilisation : !loveletter play carte_à_jouer personne_visée carte_visée")

        for line in self.loveletter.print_state().split("\n"):
            serv.privmsg(chan, "%s" % line)

