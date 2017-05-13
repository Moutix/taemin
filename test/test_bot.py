""" Test taemin bot """

import unittest

from taemin import bot

class BotTest(unittest.TestCase):
    """ Test the bot class """

    def test_initialize(self):
        """ Test intialize the bot """

        taemin = bot.Taemin()
        self.assertIsNotNone(taemin.plugins)
