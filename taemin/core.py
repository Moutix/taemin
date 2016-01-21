#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bot import Taemin
from conf import TaeminConf
import logging
import logging.handlers
import sys

__all__ = ['taemin']

class MyLogger(object):
    def __init__(self, logger, level):
        """Needs a logger and a logger level."""
        self.logger = logger
        self.level = level

    def write(self, message):
        # Only log if there is a message (not just a new line)
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())


def taemin():
    conf = TaeminConf()

    LOG_FILENAME = conf.config.get("general", {}).get("log_file", "/var/log/taemin.log")
    LOG_LEVEL = logging.INFO

    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)
    handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    sys.stdout = MyLogger(logger, logging.INFO)
    sys.stderr = MyLogger(logger, logging.ERROR)

    Taemin(conf).start()

if __name__ == "__main__":
    taemin()

