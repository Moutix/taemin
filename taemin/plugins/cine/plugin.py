#!/usr/bin/env python2
# -*- coding: utf8 -*-

import re
import urllib.parse
from datetime import date, timedelta
import json
import shlex
import itertools
from optparse import OptionParser

from bs4 import BeautifulSoup
import requests
import dateutil.parser

from taemin import plugin

class OptionParsingError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg

class CustomOptionParser(OptionParser):
    def error(self, msg):
        raise OptionParsingError(msg)

    def exit(self, status=0, msg=None):
        raise OptionParsingError(msg)

class AlloFilm(object):
    def __init__(self, id, name, year, picture, director):
        self.year = year
        self.name = name
        self.director = director
        self.id = id
        self.picture = picture
        self.link = "http://www.allocine.fr/film/fichefilm_gen_cfilm=%s.html" % self.id

    def __str__(self):
        return "<Film-%s %s (%s)>" % (self.id, self.name, self.year)

    def __repr__(self):
        return "<Film-%s %s (%s)>" % (self.id, self.name, self.year)

class AlloLocalization(object):
    def __init__(self, id, name, code):
        self.id = id
        self.name = name
        self.code = code

    def __str__(self):
        return "<Localization-%s %s (%s)>" % (self.id, self.name, self.code)

    def __repr__(self):
        return "<Localization-%s %s (%s)>" % (self.id, self.name, self.code)

class AlloSeance(object):
    MAP_VERSIONS = {"translated": "VF",
                    "original": "VO"}

    WEEK_DAY = {"lundi": 0,
                "monday": 0,
                "mardi": 1,
                "tuesday": 1,
                "mercredi": 2,
                "wednesday": 2,
                "jeudi": 3,
                "thursday": 3,
                "vendredi": 4,
                "friday": 4,
                "samedi": 5,
                "satursday": 5,
                "dimanche": 6,
                "sunday": 6}

    def __init__(self, film, localization, cine, start, end, version, quality):
        self.film = film
        self.localization = localization
        self.cine = cine
        self.start = start
        self.end = end
        self.version = self.MAP_VERSIONS.get(version, version)
        self.quality = quality

    def __str__(self):
        return "<Seance-%s %s [%s][%s]>" % (self.start, self.cine, self.version, self.quality)

    def __repr__(self):
        return "<Seance-%s %s [%s][%s]>" % (self.start, self.cine, self.version, self.quality)

    def pretty_start(self):
        return self.start.strftime("%H:%M")

    def pretty_end(self):
        return self.end.strftime("%H:%M")

    def pretty_date(self):
        return "%s-%s" % (self.pretty_start, self.pretty_end)

    def in_day(self, day):
        day = self.get_day(day)
        if self.start.date() == day:
            return True
        return False

    @classmethod
    def get_day(cls, day):
        if day in ("aujourd'hui", "today"):
            return date.today()

        if day in ("demain", "tomorrow"):
            return date.today() + timedelta(days=1)

        if day in cls.WEEK_DAY:
            iterdate = date.today()
            while True:
                if iterdate.weekday() == cls.WEEK_DAY[day]:
                    return iterdate

                iterdate += timedelta(days=1)

        return None

    @staticmethod
    def to_str(seances):
        return ", ".join(["%s (%s)(%s)" % (s.pretty_start(), s.version, s.quality) for s in seances])


class AlloCine(object):
    def __init__(self, id, id_ac, name, address):
        self.id = id
        self.id_ac = id_ac
        self.name = name
        self.address = address
        self.maps_link = "https://www.google.fr/maps/place/%s/" % urllib.parse.quote(self.address)

    def __str__(self):
        return "<cine-%s %s>" % (self.id, self.name)

    def __repr__(self):
        return "<cine-%s %s>" % (self.id, self.name)


class TaeminCine(plugin.TaeminPlugin):
    helper = {"film": "Recherche un film sur allocine. Usage !film nom",
              "seances": "Recherche des séances. Usage !seances film [--lieu=Paris] [--version] [--day=today] [--cine] [--quality] [--page=1]",
              "onscreen": "Affiche les films passant au cinéma en ce moment. Usage !onscreen page"}

    def __init__(self, taemin):
        plugin.TaeminPlugin.__init__(self, taemin)
        self.parser = self._get_opt_parser()

    def _get_opt_parser(self):
        parser = CustomOptionParser()
        parser.add_option("-l", "--lieu", type="string", dest="location", default="paris")
        parser.add_option("-q", "--quality", type="string", dest="quality")
        parser.add_option("-v", "--version", type="string", dest="version")
        parser.add_option("-d", "--day", type="string", dest="day", default="today")
        parser.add_option("-c", "--cine", type="int", dest="cine")
        parser.add_option("-p", "--page", type="int", dest="page", default=1)
        parser.add_option("--force", action="store_true", dest="force", default=False)
        return parser

    def on_pubmsg(self, msg):
        if msg.key not in ("seance", "film", "seances", "onscreen"):
            return

        chan = msg.chan.name

        if msg.key == "onscreen":
            page = 1
            if re.search(r"""\d+""", msg.value):
                page = int(msg.value)

            films = self.get_current_films(page)

            self.privmsg(chan, "Au cinéma: %s" % ", ".join(films))
            return

        if msg.key == "film":
            film = self.get_film(msg.value)
            if not film:
                self.privmsg(chan, self.helper["film"])
                return

            self.privmsg(chan, "%s - %s (%s): %s" % (film.name, film.year, film.director, film.link))
            return

        if msg.key in ("seance", "seances"):
            try:
                values = shlex.split(msg.value)
            except ValueError as msg:
                self.privmsg(chan, "Error in your args: %s" %msg)
                return

            try:
                (options, args) = self.parser.parse_args(values)
            except OptionParsingError as err:
                self.privmsg(chan, "Error in your options: %s" % err.msg)
                return

            if not options.location or not args:
                self.privmsg(chan, self.helper["seances"])
                return

            film = " ".join(args)

            if not AlloSeance.get_day(options.day):
                self.privmsg(chan, "Accepted values for day: %s" % "|".join(AlloSeance.WEEK_DAY.keys() + ["today", "tomorrow", "aujourd'hui", "demain"]))
                return

            if options.version and options.version not in AlloSeance.MAP_VERSIONS.values():
                self.privmsg(chan, "Accepted values for version %s" % "|".join(AlloSeance.MAP_VERSIONS.values()))
                return

            film = self.get_film(film)
            if not film:
                self.privmsg(chan, "Connais pas ce film.")
                return

            location = self.get_localization(options.location)
            if not location:
                self.privmsg(chan, "Lieu inconnu")
                return

            seances = [seance for seance in self.get_seances(film=film,
                                                             localization=location,
                                                             version=options.version,
                                                             day=options.day,
                                                             quality=options.quality,
                                                             cine_id=options.cine,
                                                             page=options.page)]

            self.privmsg(chan, "Seance pour le film %s (%s) à %s: %s" % (film.name, film.year, location.name, film.link))
            if not seances:
                self.privmsg(chan, "Pas de séance pour ce film avec ces paramètres")
                return

            if options.cine:
                cine = seances[0].cine
                self.privmsg(chan, "Séances pour le cinéma %s (%s): %s" % (cine.name, cine.address, cine.maps_link))
                self.privmsg(chan, AlloSeance.to_str(seances))
                return


            cines = list(set(seance.cine for seance in seances))
            if len(cines) > 3 and not options.force:
                for group_cines in [cines[i:i+10] for i in range(0, len(cines), 10)]:
                    self.privmsg(chan, ", ".join(["[%s] %s" % (cine.id, cine.name) for cine in group_cines]))
                return

            seances.sort(key=lambda x: x.cine)
            for key, seance in itertools.groupby(seances, lambda x: x.cine):
                self.privmsg(chan, "[%s] %s: %s" % (key.id, key.name, AlloSeance.to_str(seance)))

    def get_current_films(self, page=1):
        try:
            res = requests.get("http://www.allocine.fr/film/aucinema/", params={"page": page})
        except requests.RequestException:
            return []

        try:
            html = res.text
        except TypeError:
            return None

        html = BeautifulSoup(html, 'html.parser')

        return [json.loads(item["data-entities"]).get("label") for item in html.find_all('h2', attrs={'data-entities': True})]

    def get_film(self, film):
        res = self.get_films(film)
        if res:
            return res[0]
        return None

    def get_films(self, film):
        try:
            res = requests.get("http://essearch.allocine.net/fr/autocomplete", params={"q": film})
        except requests.RequestException:
            return []

        return [film for film in self.films_generator(res.json())]

    def films_generator(self, raw_result):
        if not raw_result:
            return

        for film in raw_result:
            director = None
            year = None
            if film.get("ad"):
                continue

            for meta in film.get("metadata", []):
                if meta.get("property") == "director":
                    director = meta.get("value", "")
                elif meta.get("property") == "productionyear":
                    year = meta.get("value", "")

            yield AlloFilm(film.get("id"),
                           film.get("title2", ""),
                           year,
                           film.get("poster", ""),
                           director)

    def get_localization(self, localization):
        res = self.get_localizations(localization)
        if res:
            return res[0]
        return None

    def get_localizations(self, localization):
        try:
            res = requests.get("http://www.allocine.fr/_/localization/%s" % urllib.parse.quote(localization))
        except requests.RequestException:
            return []

        return [localization for localization in self.localizations_generator(res.json())]

    def localizations_generator(self, raw_result):
        if not raw_result:
            return

        for localization in raw_result:
            yield AlloLocalization(localization.get("id"),
                                   localization.get("name", ""),
                                   localization.get("zip_code", ""))

    def get_seances(self, film, localization, version=None, day=None, quality=None, cine_id=None, page=1):
        if isinstance(film, str):
            film = self.get_film(film)
        if isinstance(localization, str):
            localization = self.get_localization(localization)
        if not film or not localization:
            return

        try:
            res = requests.get("http://www.allocine.fr/_/showtimes/movie-%s/near-%s/" % (film.id, localization.id), params={"page": page})
        except requests.RequestException:
            return

        for seance in self.seances_generator(res.json(), film, localization):
            if version and seance.version != version:
                continue

            if quality and seance.quality != quality:
                continue

            if day and not seance.in_day(day):
                continue

            if cine_id and seance.cine.id != cine_id:
                continue

            yield seance

    def seances_generator(self, raw_result, film, localization):
        theaters = {}
        if not raw_result or not raw_result.get("theaters") or not raw_result.get("showtimes"):
            return

        for id_ac, theater in raw_result.get("theaters", {}).items():
            theaters[id_ac] = AlloCine(theater.get("id"),
                                       id_ac,
                                       theater.get("name", ""),
                                       "%s. %s" % (theater.get("address", {}).get("address", ""),
                                                   theater.get("address", {}).get("city", "")))

        for id_ac, showtimes in raw_result.get("showtimes", {}).items():
            for seance in self.parse_showtimes(showtimes, theaters[id_ac], film, localization):
                yield seance

    def parse_showtimes(self, showtimes, cine, film, localization):
        for dates in showtimes.values():
            for shows in dates.values():
                for show in shows:
                    version = show.get("version", "")
                    quality = show.get("format", {}).get("name", "")
                    for s in show.get("showtimes", []):
                        yield AlloSeance(film=film,
                                         localization=localization,
                                         cine=cine,
                                         start=dateutil.parser.parse(s.get("showStart")),
                                         end=dateutil.parser.parse(s.get("movieEnd")),
                                         version=version,
                                         quality=quality)


def main():
    cine = TaeminCine(None)

    print(cine.get_films("deadpool"))
    print(cine.get_localizations("antony"))

    for seance in cine.get_seances("start", "antony", "VO", day="today", cine_id=364):
        print(seance)

    print(cine.get_current_films())

if __name__ == "__main__":
    main()
