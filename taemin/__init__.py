#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.1"

#from bot import Taemin
import conf
import database
import logging
import logging.handlers
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class MyLogger(object):
    def __init__(self, logger, level):
        """Needs a logger and a logger level."""
        self.logger = logger
        self.level = level

    def write(self, message):
        # Only log if there is a message (not just a new line)
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())

    def flush(self):
        pass


class Env(object):
    def __init__(self):
        self.conf = conf.TaeminConf().config
        db_conf = self.conf.get("database", {})

        self.db = database.DataBase(db_conf.get("type"),
                           name=db_conf.get("name"),
                           user=db_conf.get("user"),
                           password=db_conf.get("password"),
                           host=db_conf.get("host"))

        self.log = self.init_logger()

    def init_logger(self):
        filename = self.conf.get("general", {}).get("log_file", "/var/log/taemin.log")
        level = logging.INFO

        logger = logging.getLogger(__name__)
        logger.setLevel(level)
        handler = logging.handlers.TimedRotatingFileHandler(filename, when="midnight", backupCount=3)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        sys.stdout = MyLogger(logger, logging.INFO)
        sys.stderr = MyLogger(logger, logging.ERROR)
        return logger

env = Env()
