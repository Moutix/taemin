#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import os
import sys
import glob

from setuptools import setup, find_packages

import taemin

for filename in glob.glob("cfg/*.yml*"):
    shutil.copy(filename, "smserver/_fallback_conf")

CONF_DIR = None

if os.path.splitdrive(sys.executable)[0] != "":
    CONF_DIR = "conf"

if not CONF_DIR and os.path.isdir("/etc/taemin"):
    CONF_DIR = "/etc/taemin"

if not CONF_DIR:
    try:
        os.mkdir("/etc/taemin")
        CONF_DIR = "/etc/taemin"
    except:
        pass

if not CONF_DIR:
    CONF_DIR = "conf"

setup(
    name='taemin',

    version=taemin.__version__,

    packages=find_packages(),

    author="Sélim Menouar",

    author_email="selim.menouar@rez-gif.supelec.fr",

    description="Le plus bot du monde",

    long_description=open('README.md').read(),

    include_package_data=True,

    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Topic :: Games/Entertainment',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
    ],

    install_requires=[
        'irc',
        'peewee',
        'bs4',
        'feedparser',
        'requests',
        'romkan',
    ],

    url='http://github.com/ningirsu/taemin',

    license="MIT",

    scripts=["scripts/taemin"],

    data_files=[(CONF_DIR, ['conf/conf.yml.orig'])],
)
