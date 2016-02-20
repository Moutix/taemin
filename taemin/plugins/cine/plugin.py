#!/usr/bin/env python2
# -*- coding: utf8 -*-

import requests
import urllib
import dateutil.parser
from datetime import date, timedelta
import shlex
from optparse import OptionParser
import itertools

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


class AlloCine(object):
    def __init__(self, id, id_ac, name, address):
        self.id = id
        self.id_ac = id_ac
        self.name = name
        self.address = address

    def __str__(self):
        return "<Cine-%s %s>" % (self.id, self.name)

class TaeminCine(object):
    helper = {"film": "Recherche un film sur allocine. Usage !film nom",
              "seances": "Recherche des séances de cinéma. Usage !seance --film --lieu --quality=[VF|VO], --day --cine"}

    def __init__(self, taemin):
        self.taemin = taemin
        self.parser = self._get_opt_parser()

    def _get_opt_parser(self):
        parser = CustomOptionParser()
        parser.add_option("-f", "--film", type="string", dest="film")
        parser.add_option("-l", "--lieu", type="string", dest="location", default="paris")
        parser.add_option("-q", "--quality", type="string", dest="quality")
        parser.add_option("-v", "--version", type="string", dest="version")
        parser.add_option("-d", "--day", type="string", dest="day", default="today")
        parser.add_option("-c", "--cine", type="int", dest="cine_id")
        return parser

    def on_pubmsg(self, serv, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        if msg.key == "film":
            film = self.get_film(msg.value)
            if not film:
                serv.privmsg(chan, self.helper["film"])
                return

            serv.privmsg(chan, "%s - %s (%s): %s" % (film.name, film.year, film.director, film.link))
            return

        if msg.key == "seances":
            try:
                (options, arg) = self.parser.parse_args(shlex.split(msg.value))
            except OptionParsingError as err:
                serv.privmsg(chan, "Error in your options: %s" % err)
                return

            if not options.film or not options.location:
                serv.privmsg(chan, "Film and Location are mandatory. Use -f|--film and -l|--lieu")
                return

            if not AlloSeance.get_day(options.day):
                serv.privmsg(chan, "Accepted values for day: %s" % "|".join(AlloSeance.WEEK_DAY.keys() + ["today", "tomorrow", "aujourd'hui", "demain"]))
                return

            if options.version and options.version not in AlloSeance.MAP_VERSIONS.values():
                serv.privmsg(chan, "Accepted values for version %s" % "|".join(AlloSeance.MAP_VERSIONS.values()))
                return

            film = self.get_film(options.film)
            location = self.get_localization(options.location)

            seances = [seance for seance in self.get_seances(film=film,
                                                             localization=location,
                                                             version=options.version,
                                                             day=options.day,
                                                             quality=options.quality)]
            serv.privmsg(chan, "Seance pour le film %s (%s) à %s: %s" % (film.name, film.year, location.name, film.link))
            if not seances:
                serv.privmsg(chan, "Pas de séance pour ce film avec ces paramètres")
                return

            seances.sort(cmp=lambda x, y: cmp(x.cine, y.cine))
            for key, seance in itertools.groupby(seances, lambda x: x.cine):
                serv.privmsg(chan, "[%s] %s: %s" % (key.id, key.name, " ".join(["(%s): %s" % (s.version, s.pretty_start()) for s in seance])))


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

        return [film for film in self.films_generator(res.json)]

    def films_generator(self, raw_result):
        if not raw_result:
            return

        for film in raw_result:
            director = None
            year = None
            for meta in film.get("metadata", []):
                if meta.get("property") == "director":
                    director = meta.get("value", "").encode("utf-8")
                elif meta.get("property") == "productionyear":
                    year = meta.get("value", "").encode("utf-8")

            yield AlloFilm(film.get("id"),
                           film.get("title2", "").encode("utf-8"),
                           year,
                           film.get("poster", "").encode("utf-8"),
                           director)

    def get_localization(self, localization):
        res = self.get_localizations(localization)
        if res:
            return res[0]
        return None

    def get_localizations(self, localization):
        try:
            res = requests.get("http://www.allocine.fr/_/localization/%s" % urllib.quote(localization))
        except requests.RequestException:
            return []

        return [localization for localization in self.localizations_generator(res.json)]

    def localizations_generator(self, raw_result):
        if not raw_result:
            return

        for localization in raw_result:
            yield AlloLocalization(localization.get("id"),
                                   localization.get("name", "").encode("utf-8"),
                                   localization.get("zip_code", "").encode("utf-8"))

    def get_seances(self, film, localization, version=None, day=None, quality=None, cine_id=None):
        if isinstance(film, str):
            film = self.get_film(film)
        if isinstance(localization, str):
            localization = self.get_localization(localization)
        if not film or not localization:
            return

        try:
            res = requests.get("http://www.allocine.fr/_/showtimes/movie-%s/near-%s/" % (film.id, localization.id))
        except requests.RequestException:
            return

        for seance in self.seances_generator(res.json, film, localization):
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

        for id_ac, theater in raw_result.get("theaters", {}).iteritems():
            theaters[id_ac] = AlloCine(theater.get("id"),
                                       id_ac,
                                       theater.get("name", "").encode("utf-8"),
                                       "%s. %s" % (theater.get("address", {}).get("address", "").encode("utf-8"),
                                                   theater.get("address", {}).get("city", "").encode("utf-8")))

        for id_ac, showtimes in raw_result.get("showtimes", {}).iteritems():
            for seance in self.parse_showtimes(showtimes, theaters[id_ac], film, localization):
                yield seance

    def parse_showtimes(self, showtimes, cine, film, localization):
        for dates in showtimes.itervalues():
            for shows in dates.itervalues():
                for show in shows:
                    version = show.get("version", "").encode("utf-8")
                    quality = show.get("format", {}).get("name", "").encode("utf-8")
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

    print cine.get_films("")
    print cine.get_localizations("antony")

    for seance in cine.get_seances("start", "antony", "VO", day="today", cine_id=364):
        print seance

if __name__ == "__main__":
    main()

