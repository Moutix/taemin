#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import os
import sys
import glob

from setuptools import setup, find_packages

import taemin

for filename in glob.glob("conf/*.yml*"):
    shutil.copy(filename, "taemin/_fallback_conf")

if os.path.splitdrive(sys.executable)[0] == "":
    conf_dir = "/etc/taemin"
else:
    conf_dir = "conf"

setup(
    name='taemin',

    version=taemin.__version__,

    packages=find_packages(),

    author="Sélim Menouar",

    author_email="selim.menouar@rez-gif.supelec.fr",

    description="Le plus bot du monde",

    long_description=open('README.md').read(),

    include_package_data=True,

    url='http://github.com/ningirsu/taemin',

    license="MIT",

    scripts=["scripts/taemin"],

    data_files=[(conf_dir, ['conf/conf.yml.orig'])],
)
