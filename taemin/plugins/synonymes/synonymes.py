#!/usr/bin/env python2
# -*- coding: utf8 -*-

import urllib.parse
from bs4 import BeautifulSoup
import requests

class Synonymes(object):
    URL = "http://www.crisco.unicaen.fr/des/synonymes"
    SELECTOR = "#synonymes td > a"

    def __init__(self, word):
        self.word = word
        self.synonymes = self.off(word)

    @classmethod
    def off(cls, word):
        soup = cls._get_html(word)

        return [s.getText().strip() for s in soup.select(cls.SELECTOR)]

    @classmethod
    def _get_html(cls, word):
        try:
            res = requests.get("%s/%s" % (cls.URL, urllib.parse.quote(word))).text
        except requests.RequestException:
            return None

        return BeautifulSoup(res, 'html.parser')

def main():
    print(Synonymes.off("test"))
    print(Synonymes.off("machin"))
    print(Synonymes("mémé").synonymes)
    print(Synonymes.off("méazd"))

if __name__ == "__main__":
    main()
