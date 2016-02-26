#!/usr/bin/env python2
# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
import requests
import logging
import urllib

class Dico(object):
    URL = "http://www.larousse.fr/dictionnaires/rechercher"
    def __init__(self, word):
        self.word = word
        self._html = self._get_html()
        self.definition = self._find_definition(self._html)
        self.descriptions = self._find_descriptions(self._html)
        self.description = self.descriptions[0] if self.descriptions else None
        self.suggestions = self._find_suggestions(self._html)
        self.suggestion = self.suggestions[0] if self.suggestions else None

    def _get_html(self):
        try:
            res = requests.get("%s?q=%s&l=francais&culture=" % (self.URL, urllib.quote(self.word))).text
        except requests.RequestException:
            return None

        return BeautifulSoup(res, 'html.parser')

    def _find_suggestions(self, html):
        return [item.getText().encode("utf-8") for item in html.select("section.corrector ul > li > h3 > a")]

    def _find_descriptions(self, html):
        return [item.getText().encode("utf-8") for item in html.find_all("li", {"class": "DivisionDefinition"})]

    def _find_definition(self, html):
        definition = html.find("p", {"class": "CatgramDefinition"})
        if not definition:
            return None
        return definition.getText().encode("utf-8")

def main():
    dico = Dico("mémé")
    print dico.suggestions
    print dico.definition
    print dico.descriptions

if __name__ == "__main__":
    main()


