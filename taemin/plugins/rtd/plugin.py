#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin
from random import randint
from re import split,finditer

class TaeminRTD(plugin.TaeminPlugin):
    helper = {
        "rtd": "Roll The Dice",
        "rand": "Random number between 1 and 20",
        "random": "Random number between 1 and 100"
    }
    
    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name
        
        if msg.key == "random":
            di = 100
            self.privmsg(chan, "%s => %s"%(msg.key, randint(1,di)))
        else if msg.key == "rand":
            di = 20
            self.privmsg(chan, "%s => %s"%(msg.key, randint(1,di)))
        else :
            if msg.value == "" :
                di = 6
                self.privmsg(chan, "%s => %s"%(msg.key, randint(1,di)))
                return
                
            for nbDdi_ in finditer('[0-9]+[dD]?[0-9]+', msg.value):
                nbDdi = nbDdi_.group()
                li = split('[dD]', nbDdi)
                if length(li) > 1:
                    nb = int(li[0])
                    di = int(li[1])
                else :
                    di = int(li[0])
                
                message = " ".join([str(randint(1,di)) for i in range(0,nb)])
                self.privmsg(chan, "%s %s => %s"%(msg.key, nbDdi, message))