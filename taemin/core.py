#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bot import Taemin
from conf import TaeminConf

__all__ = ['taemin']

def taemin():
    conf = TaeminConf()
    Taemin(conf).start()

if __name__ == "__main__":
    taemin()

