""" Commont test file """

import unittest

from taemin import conf

conf.get_config("taemin").load("-c", "test/conf.yml")

from taemin import bot

class TaeminTest(unittest.TestCase):
    """ Base for all test """
    def setUp(self):
        self.taemin = bot.Taemin("-c", "test/conf.yml")
