#!/usr/bin/env python2
# -*- coding: utf8 -*-

from io import open
import argparse
import yaml
import sys
import os

class TaeminConf(dict):
    """
        Configuration dictionnary.

        It use yaml configuration file by default, and some option can be
        change by passing it in argument (with argparse)
    """

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    _fallback_conf = os.path.join(__location__, "_fallback_conf/conf.yml.orig")

    def __init__(self, *args):
        self.parser = argparse.ArgumentParser(description='Taemin configuration')

        dict.__init__(self)

        self.parser.add_argument(
            '-c', '--config',
            dest='config',
            help="Server's configuration file (default: %s)" % self._default_conf(),
            default=self._default_conf()
        )

        self._raw_args = None
        self._args = None

        self.load(*args)

    def load(self, *args):
        self._raw_args = args
        self._args = self.parser.parse_args(args)
        default_arg = self.parser.parse_args([])

        configuration_file = self._find_configuration_file(self._args.config)

        with open(configuration_file, 'r', encoding='utf-8') as stream:
            self.update(yaml.load(stream), allow_unicode=True)

        for key, value in vars(self._args).items():
            self.add_to_conf(self, key, value, getattr(default_arg, key, None) != value)

    def reload(self):
        """ Reload the configuration file """

        self.__init__(*self._raw_args)

    @staticmethod
    def add_to_conf(conf, arg, value, replace=True):
        """
            Add the given value to the conf

            :param dict conf: The configuration dictionnary
            :param str arg: The path of the key, with dot notation
            :param value: Value to assign
            :param bool replace: If the key already exist replace it

            :Example:

            >>> conf = {}
            >>> Conf.add_to_conf(conf, "root.key", "value")
            >>> print(conf)
            {'root': {'key': 'value'}}

            >>> Conf.add_to_conf(conf, "root.key", "new_value", replace=False)
            >>> print(conf)
            {'root': {'key': 'value'}}

            >>> Conf.add_to_conf(conf, "root.key", "new_value", replace=True)
            >>> print(conf)
            {'root': {'key': 'new_value'}}
        """

        arg = arg.split(".")
        arg.reverse()
        while True:
            option = arg.pop()
            if not arg:
                if replace or option not in conf:
                    conf[option] = value
                return

            if option not in conf:
                conf[option] = {}

            conf = conf[option]

    @classmethod
    def _default_conf(cls):
        if os.path.splitdrive(sys.executable)[0] == "":
            return "/etc/taemin/conf.yml"

        return "conf.yml"

    @classmethod
    def _find_configuration_file(cls, path):
        if os.path.isfile(path):
            return path

        if os.path.isfile(path + ".orig"):
            return path + ".orig"

        return cls._fallback_conf

_CONFIG = {}

def get_config(name):
    if name not in _CONFIG:
        _CONFIG[name] = TaeminConf()

    return _CONFIG[name]

if __name__ == "__main__":
    print(TaeminConf(*sys.argv[1:]))
