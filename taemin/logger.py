""" Logging module """

import logging
import logging.handlers
import sys
import traceback

from taemin import conf

class Logger(logging.Logger):
    _LEVEL = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    def __init__(self):
        logging.Logger.__init__(self, __name__)
        self._conf = conf.get_config("taemin").get("general", {})

        self.setLevel(self._LEVEL.get(self._conf.get("log_level"), logging.INFO))
        self.addHandler(self._get_handler())
        self.addHandler(logging.StreamHandler(sys.stdout))

    def _get_handler(self):
        filename = self._conf.get("log_file", "/var/log/taemin.log")
        handler = logging.handlers.TimedRotatingFileHandler(filename, when="midnight", backupCount=3)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        return handler

if __name__ == "__main__":
    log = Logger()
    log.info("coucou")
