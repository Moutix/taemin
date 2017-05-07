#!/usr/bin/env python2
# -*- coding: utf8 -*-

import random

from taemin import plugin
from .shifumi_schema import Shifumi

class TaeminShifumi(plugin.TaeminPlugin):
    helper = {"shifumi": "Play shifumi: !shifumi rock|scissor|paper"}
    data = {"rock": "scissor",
            "scissor": "paper",
            "paper": "rock"}

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        if msg.value not in ("rock", "scissor", "paper"):
            self.privmsg(chan, self.helper[msg.key])
            return

        value = self.play(msg.value, msg.user)
        self.privmsg(chan, "%s ! %s" % (
            value,
            self.pretty_who_win(value, msg.value)))

    def play(self, value, user=None):
        my_value = self.guess_play(value, user)
        if not my_value:
            my_value = random.choice(list(self.data))

        self.save(my_value, value, user)

        return my_value

    @classmethod
    def save(cls, my_value, user_value, user=None):
        Shifumi.create(
                user=user,
                my_value=my_value,
                user_value=user_value,
                winner=cls.who_win(my_value, user_value))

    def guess_play(self, value, user=None):
        """ To do """
        return None

    @classmethod
    def who_win(cls, value1, value2):
        if cls.data[value1] == value2:
            return "me"

        if cls.data[value2] == value1:
            return "you"

        return "tie"

    @classmethod
    def pretty_who_win(cls, my_value, user_value):
        value = cls.who_win(my_value, user_value)

        if value == "me":
            return "J'ai gagné :p"

        if value == "you":
            return "Tssssk"

        return "Pareil..."

if __name__ == "__main__":
    print(TaeminShifumi(None).play("rock"))
    print(TaeminShifumi(None).play("rock"))
