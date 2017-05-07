#!/usr/bin/env python2
# -*- coding: utf8 -*-

import time
from taemin import plugin

class TaeminPause(plugin.TaeminPlugin):
    helper = {"pause": "Compte le temps passé en pause ;). Usage: !pause start|stop|restart"}

    def __init__(self, taemin):
        plugin.TaeminPlugin.__init__(self, taemin)
        self.users = {}

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        user = msg.user.name

        if user not in self.users:
            self.users[user] = {"pause": 0, "last_start": None}

        chan = msg.chan.name

        if msg.value == "start":
            if self.users[user]["last_start"]:
                self.privmsg(chan, "Ta pause a déjà commencé, profites en !! ;)")
                return

            self.users[user]["last_start"] = time.time()
            self.privmsg(chan, "Debut de la pause ! Bouge toi ! ;)")
            return

        if msg.value == "stop":
            if not self.users[user]["last_start"]:
                self.privmsg(chan, "La pause a pas encore commencé...")
                return

            self.users[user]["pause"] = self.get_pause_time(user)
            this_pause = self.get_current_pause_time(user)
            self.users[user]["last_start"] = None
            if this_pause > 29:
                self.privmsg(chan, "Et la règle des 29 minutes ? !!! Tu as passé %s de ton temps en pause !" % self.display_pause(this_pause))
                return

            self.privmsg(chan, "Fin de la pause :(. Temps passé: %s" % self.display_pause(this_pause))
            return

        if msg.value == "restart":
            self.users[user]["last_start"] = None
            self.users[user]["pause"] = 0
            self.privmsg(chan, "Temps de pause redémarré !")
            return

        if self.get_pause_time(user) < 3600:
            self.privmsg(chan, "Temps en pause : %s. Tu peux y aller. ;)" % self.display_pause(self.get_pause_time(user)))
            return

        self.privmsg(chan, "Temps en pause : %s. Va falloir arrêter les pauses là ! :p" % self.display_pause(self.get_pause_time(user)))

    def get_current_pause_time(self, user):
        if self.users[user]["last_start"]:
            return time.time() - self.users[user]["last_start"]
        return self.users[user]["pause"]

    def get_pause_time(self, user):
        if self.users[user]["last_start"]:
            return self.users[user]["pause"] + time.time() - self.users[user]["last_start"]
        return self.users[user]["pause"]

    def display_pause(self, pause):
        ptime = time.gmtime(pause)
        if pause < 60:
            return time.strftime("%S secondes", ptime)
        if pause < 3600:
            return time.strftime("%M minutes et %S secondes", ptime)
        if pause < 3600*24:
            return time.strftime("%H heures et %M minutes", ptime)
        return time.strftime("%d jours et %H heures", ptime)
