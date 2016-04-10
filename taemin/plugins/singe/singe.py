#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import os

class Singe(object):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    DICO_FILE = (os.path.join(__location__, "dico.txt"))

    LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "-"]
    with open(DICO_FILE, 'r') as content_file:
        DICO = content_file.read().split("\n")
 
    def __init__(self):
        self.start_word = ""
        self.available_words = self.DICO
        self.victory = None

    def add_letter(self, letter):
        letter = letter.upper()
        if letter not in self.LETTERS:
            raise NameError("La lettre %s n'est pas possible" % letter)

        start_word = self.start_word + letter
        available_words = [w for w in self.available_words if len(w) >= len(start_word) and w[:len(start_word)].upper() == start_word]

        if not available_words:
            return False
        else:
            self.available_words = available_words
            self.start_word = start_word
            return True

    def play(self):
        words = self.next_words()
        if not words:
            return False
        else:
            word = random.choice(words)
            return self.add_letter(word[len(self.start_word)])

    def next_words(self):
        return [w for w in self.available_words if len(w) > len(self.start_word)]

    def word(self):
        return random.choice(self.available_words)

    def restart(self):
        self.__init__()


if __name__ == "__main__":
    singe = Singe()
    while singe.victory is None:
        print("taemin joue")
        singe.play()
        print(singe.start_word)
        print("A joue")
        singe.add_letter("A")
        print(singe.start_word)

    print("victory: " + str(singe.victory))
    print(singe.word())

