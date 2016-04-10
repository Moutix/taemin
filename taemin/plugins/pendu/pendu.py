#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Mon super Pendu """

import random
import os

class Pendu(object):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    DICO = os.path.join(__location__, "dico.txt")
    FOLDER = os.path.join(__location__, "images")
    LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    def __init__(self, min_letter=6, word=None):
        self.min_letter = min_letter
        self.word = word or self.find_word()
        self.attempt = []
        self.attempt_failed = 0
        self.max_attempt = 11
        self.victory = None

    def find_word(self):
        with open(self.DICO, 'r') as content_file:
            content = [w for w in content_file.read().split("\n") if len(w) >= self.min_letter]

        if content:
            word = random.choice(content)
        else:
            self.min_letter = 6
            word = self.find_word()

        return word

    def new_word(self, min_letter=6, word=None):
        self.__init__(min_letter, word)

    def test(self, word):
        if word.upper() in self.LETTERS:
            return self.try_letter(word)
        else:
            return self.try_word(word)

    def try_word(self, word):
        if word.lower() == self.word:
            self.victory = True
            return True
        else:
            self.attempt_failed += 1
            if self.attempt_failed >= self.max_attempt:
                self.victory = False
            return False

    def try_letter(self, letter):
        letter = letter.upper()
        if letter not in self.LETTERS:
            raise NameError("La lettre %s n'est pas possible" % letter)

        if letter in self.attempt:
            raise NameError("La lettre %s a déjà été essayée" % letter)

        self.attempt.append(letter)
        if letter in self.word.upper():
            test = True
            for l in self.word:
                if l.upper() not in self.attempt and l.upper() in self.LETTERS:
                    test = False
            if test:
                self.victory = True
            return True
        else:
            self.attempt_failed += 1
            if self.attempt_failed >= self.max_attempt:
                self.victory = False

            return False

    def print_word(self):
        word = []
        for letter in self.word:
            letter = letter.upper()
            if letter in self.attempt or letter not in self.LETTERS:
                word.append(letter)
            else:
                word.append("_")
        return " ".join(word)

    def print_pendu(self):
        number = self.attempt_failed
        if number >= self.max_attempt:
            number = self.max_attempt

        with open("%s/%s.txt" %(self.FOLDER, str(number)), 'r') as content_file:
            return content_file.read()

    def pretty_print(self):
        return "%s\n%s\n(%s)" % (self.print_pendu(), self.print_word(), " ".join(self.attempt))

if __name__ == "__main__":
    pendu = Pendu("15")
    print(pendu.word)
    print(pendu.pretty_print())
    pendu.try_letter("A")
    print(pendu.pretty_print())
    pendu.try_letter("E")
    print(pendu.pretty_print())
    pendu.try_letter("I")
    print(pendu.pretty_print())
    pendu.try_letter("O")
    print(pendu.pretty_print())
    pendu.try_letter("U")
    print(pendu.pretty_print())

