""" Test morpion module """

import unittest

from taemin.plugins.morpion import morpion

class MorpionTest(unittest.TestCase):
    """ Class to test the morpion """

    def test_initalizer(self):
        """ Test the initialization of the game """

        game = morpion.Morpion(size=2)

        self.assertEqual(game.matrix, [
            [None, None],
            [None, None],
        ])

        game = morpion.Morpion(size=3)

        self.assertEqual(game.matrix, [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ])

    def test_play(self):
        """ Test to place an element on the grid """

        game = morpion.Morpion(size=3)

        self.assertTrue(game.play(1, 1, 1))

        self.assertEqual(game.matrix, [
            [None, None, None],
            [None, 1, None],
            [None, None, None],
        ])

        self.assertFalse(game.play(1, 1, 1))
        self.assertFalse(game.play(1, 3, 1))
        self.assertFalse(game.play(3, 1, 1))

        self.assertEqual(game.matrix, [
            [None, None, None],
            [None, 1, None],
            [None, None, None],
        ])

    def test_reset(self):
        """ Test reinitialize the game """

        game = morpion.Morpion(size=3)

        game.matrix = [
            [0, None, None],
            [None, 1, None],
            [None, None, 0],
        ]

        game.reset()
        self.assertEqual(game.matrix, [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ])

    def test_iter_line(self):
        """ test itering on each line of the game """

        game = morpion.Morpion(size=3)

        game.matrix = [
            [0, None, 1],
            [None, 1, 0],
            [None, None, 0],
        ]

        self.assertEqual(game.matrix, [line for line in game.iter_line()])

    def test_iter_column(self):
        """ test itering on each line of the game """

        game = morpion.Morpion(size=3)

        game.matrix = [
            [0, None, 0],
            [None, 1, 1],
            [None, None, 0],
        ]

        self.assertEqual(
            [
                [0, None, None],
                [None, 1, None],
                [0, 1, 0],
            ],
            [col for col in game.iter_column()]
        )

    def test_iter_diagonal(self):
        """ test itering on each diagonal of the game """

        game = morpion.Morpion(size=3)

        game.matrix = [
            [0, None, 0],
            [None, 1, 1],
            [None, None, 0],
        ]

        self.assertEqual(
            [
                [0, 1, 0],
                [None, 1, 0],
            ],
            [diag for diag in game.iter_diagonal()]
        )

    def test_check_victory(self):
        """ Check if someone have gain the game """

        game = morpion.Morpion(size=3)
        self.assertEqual(game.winner(), None)

        game.matrix = [
            [0, None, None],
            [None, 1, None],
            [None, None, 0],
        ]
        self.assertEqual(game.winner(), None)

        game.matrix = [
            [0, None, None],
            [1, 1, 1],
            [None, None, 0],
        ]
        self.assertEqual(game.winner(), 1)

        game.matrix = [
            [0, None, None],
            [1, 0, 1],
            [None, None, 0],
        ]
        self.assertEqual(game.winner(), 0)

        game.matrix = [
            [0, 1, 0],
            [0, 1, 1],
            [1, 0, 0],
        ]
        self.assertEqual(game.winner(), None)

        game.matrix = [
            [0, 1, 0],
            [0, 1, 1],
            [1, 1, 0],
        ]
        self.assertEqual(game.winner(), 1)

        game.matrix = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 0],
        ]
        self.assertEqual(game.winner(), 0)
