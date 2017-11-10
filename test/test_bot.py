""" Test taemin bot """

from test import utils

class BotTest(utils.TaeminTest):
    """ Test the bot class """

    def test_initialize(self):
        """ Test intialize the bot """

        self.assertIsNotNone(self.taemin.plugins)
