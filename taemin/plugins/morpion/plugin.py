""" Morpion plugin """

from taemin import plugin
from taemin.plugins.morpion import morpion

class TaeminMorpion(plugin.TaeminPlugin):
    """ Interface to the morpion """

    helper = {"morpion": "Play morpion. Use !morpion line col|start [size]"}

    def __init__(self, taemin):
        super().__init__(taemin)

        self.morpions = {}

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan_name = msg.chan.name

        if not msg.value.strip():
            self.privmsg(chan_name, self.helper[msg.key])
            return

        svalue = msg.value.split(" ", 1)
        if svalue[0].lower() == "start":
            size = 3
            if len(svalue) == 2:
                try:
                    size = int(svalue[1])
                except ValueError:
                    size = -1

            if size <= 0:
                self.privmsg(chan_name, "Invalid size of the morpion")
                return

            self.morpions[chan_name] = morpion.Morpion(size)
            self.privmsg(chan_name, "New morpion start (size=%s)" % size)
            return

        if chan_name not in self.morpions:
            self.privmsg(chan_name, "No morpion game started. Use !morpion start [size=3] to start a game")
            return

        if len(svalue) != 2:
            self.privmsg(chan_name, self.helper[msg.hey])
            return

        self.play(chan_name, svalue[0], svalue[1], msg.user.name)

    def display_morpion(self, chan):
        """ Send to IRC the state of the game """

        for line in self.morpions[chan].iter_line():
            self.privmsg(
                chan,
                " | ".join(
                    str(elem) if elem is not None else "  " for elem in line
                )
            )

    def play(self, chan, line, col, user):
        """ Try to play on the morpion """

        game = self.morpions[chan]

        try:
            line = int(line)
            col = int(col)
        except ValueError:
            self.privmsg(chan, "Invalid line or col pass")
            return

        res = game.play(line, col, user)
        if not res:
            self.privmsg(chan, "Invalid line or col pass")
            return

        if game.winner() is not None:
            self.privmsg(chan, "%s win the game!" % game.winner())
            self.display_morpion(chan)
            game.reset()
            return

        self.display_morpion(chan)
