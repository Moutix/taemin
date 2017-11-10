""" Test taemin plugin """

import mock

from taemin import plugin

from test import utils

class TaeminPluginTest(utils.TaeminTest):
    """ test TaeminPlugin class """ 

    def setUp(self):
        super().setUp()
        self.plugin = plugin.TaeminPlugin(self.taemin)

    @mock.patch("irc.client.ServerConnection.privmsg")
    def test_privmsg(self, privmsg):
        self.plugin.privmsg("#bla", "bla")
        privmsg.assert_called_with("#bla", "bla")

        privmsg.reset_mock()


        self.plugin.privmsg("#bla", b"\x00")
        privmsg.assert_called_with("#bla", "\x00")
