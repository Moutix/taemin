#!/usr/bin/env python2
# -*- coding: utf8 -*-

import yaml
import os
import glob

class TaeminConf(object):
    CONF_FILE = "taemin.yml"
    def __init__(self):
        self.config = {}
        self.add_to_conf(self.CONF_FILE)
        self.plugin_confs = self.check_for_conf()
        for conf in self.plugin_confs:
            self.add_to_conf(conf)

    def add_to_conf(self, conf_file):
        self.config.update(yaml.load(file(conf_file, 'r')))

    def check_for_conf(self):
        conf_file = []
        for path in self.config.get("plugins", {}).iterkeys():
            dirpath = os.path.dirname(path.replace(".", "/"))
            conf_file.extend(glob.glob(dirpath + "/*.yml"))
        return conf_file

if __name__ == "__main__":
    print TaeminConf().config
