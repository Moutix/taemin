#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import plugin
from random import randint
import re

class TaeminRTD(plugin.TaeminPlugin):
    helper = {
        "rtd": "Roll The Dice: '!rtd [[[X]d]Y]' casts X Y-sides dice",
        "rand": "Random number between 1 and 20",
        "random": "Random number between 1 and 100"
    }

    _default_values = {"rtd" : "6", "rand" : "20", "random" : "100"}


    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        if msg.key == "rtd" and msg.value != "" :
            messages = self._cast_dice(msg.value)
        else :
            messages = self._cast_dice(self._default_values[msg.key])

        for message in messages:
            self.privmsg(chan, message)


    def _cast_dice(self, dice_sets, _regex = re.compile('[0-9]*[dD]?[0-9]+')):
        for dice_set_ in _regex.finditer(dice_sets):
            dice_set = dice_set_.group().upper()
            count_sides = map(int, filter(None, dice_set.split('D')))
            if len(count_sides) > 1:
                count = count_sides[0]
                sides = count_sides[1]
            else :
                count = 1
                sides = count_sides[0]

            result = " ".join([str(randint(1, sides)) for _ in range(count)])
            yield "RTD(%s) => %s" % (dice_set, result)