#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
    Kick Vote Plugin
"""

import time
from threading import Thread

from taemin import plugin

class TaeminVoxPopuli(plugin.TaeminPlugin):
    """ Vox Populi Plugin """

    helper = {
        "voxpopuli": "Vote to kick someone: '!voxpopuli [nick] [vote duration (s)]",
    }

    def __init__(self, taemin):
        plugin.TaeminPlugin.__init__(self, taemin)
        self.states = {}

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        if chan not in self.states:
            self.states[chan] = VoxWait(self, chan)

        if msg.key == "voxpopuli":
            self.swap_state(chan, self.states[chan].on_msg(msg.value, msg.user.name))

    def on_timeout(self, chan):
        """ Called once the vote is finished """

        if chan not in self.states:
            return

        self.swap_state(chan, self.states[chan].on_timeout())

    def swap_state(self, chan, new_state):
        """ Swap to a new state """

        if new_state is not None:
            self.states[chan] = new_state


class VoxState(object):
    """ State for the Plugin """

    _default_values = {"duration" : "120", "nick" : "FlyingYeti"}

    def __init__(self, _plugin, chan):
        self.plugin = _plugin
        self.chan = chan

    def on_msg(self, msg, author):
        """ Called when the voxpopuli receives a command """
        pass

    def on_timeout(self):
        """ Called once the vote is finished """
        pass

    def fork(self, constructor, *args):
        """ Create another state for the same chan """
        return constructor(self.plugin, self.chan, *args)


class VoteTimer(Thread):
    """ Timer for the Vote """
    def __init__(self, _time, _plugin, chan):
        Thread.__init__(self)
        self.plugin = _plugin
        self.chan = chan
        self._time = _time

    def run(self):
        time.sleep(self._time)
        self.plugin.on_timeout(self.chan)


class VoxWait(VoxState):
    """ Wait for a Vote to be started """

    def on_msg(self, msg, author):

        # Parse the Arguments
        tokens = msg.strip().split(" ") if msg != "" else []

        nick = VoxState._default_values["nick"]
        duration = VoxState._default_values["duration"]

        try:
            nick = tokens.pop(0)
            duration = tokens.pop(0)
        except IndexError:
            pass

        #TODO: Verify if the nick is in the chan

        # Parse the Duration
        try:
            duration = int(float(duration))
        except ValueError:
            duration = int(float(VoxState._default_values["duration"]))

        return self.fork(VoxVote, nick, duration)


class VoxVote(VoxState):
    """ Collect the votes """

    def __init__(self, _plugin, chan, nick, duration):
        VoxState.__init__(self, _plugin, chan)

        self.nick = nick

        timer = VoteTimer(duration, self.plugin, self.chan)
        timer.start()

        self.votes = {}
        self.plugin.privmsg(
            self.chan, "Starting Vote to kick {}. Duration: {} seconds.".format(
                self.nick, duration)
            )

    def on_timeout(self):
        total = len(self.votes)
        yes = len([x for x in self.votes.values() if x is True])

        self.plugin.privmsg(
            self.chan, "Result of the Vote to kick {}. Yes: {}, No: {}.".format(
                self.nick, yes, total - yes)
            )

        if yes > int(total/2):
            self.plugin.kick(self.chan, self.nick, "Mouhahaha")

        return self.fork(VoxWait)

    def on_msg(self, msg, author):

        if author in self.votes:
            return self

        self.votes[author] = bool(msg == "yes")

        return self
