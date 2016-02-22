#!/usr/bin/env python2
# -*- coding: utf8 -*-

import time

class TaeminPause(object):
    helper = {"pause": "Compte le temps passer en pause ;). Usage: !pause start|stop|restart"}

    def __init__(self, taemin):
        self.taemin = taemin
        self.pause = 0
        self.last_start = None


    def on_pubmsg(self, serv, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        if msg.value == "start":
            if self.last_start:
                serv.privmsg(chan, "La pause a déjà commencé, profites en !! ;)")
                return

            self.last_start = time.time()
            serv.privmsg(chan, "Debut de la pause ! On se bouge ;)")
            return

        if msg.value == "stop":
            if not self.last_start:
                serv.privmsg(chan, "La pause a pas encore commencé...")
                return

            self.pause = self.get_pause_time()
            self.last_start = None
            serv.privmsg(chan, "Fin de la pause :(. Temps passé: %s" % self.display_pause())
            return

        if msg.value == "restart":
            self.last_start = None
            self.pause = 0
            serv.privmsg(chan, "Temps de pause redémarré !")
            return

        serv.privmsg(chan, "Temps en pause : %s" % self.display_pause())

    def get_pause_time(self):
        if self.last_start:
            return self.pause + time.time() - self.last_start
        return self.pause

    def display_pause(self):
        pause_sec = self.get_pause_time()
        pause = time.gmtime(pause_sec)
        if pause_sec < 60:
            return time.strftime("%S secondes", pause)
        if pause_sec < 3600:
            return time.strftime("%M minutes et %S secondes", pause)
        if pause_sec < 3600*24:
            return time.strftime("%H heures et %M minutes" , pause)
        return time.strftime("%d jours et %H heures" , pause)

