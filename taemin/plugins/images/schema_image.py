#!/usr/bin/env python2
#-*- coding: utf8 -*-

from taemin import env, schema
from peewee import *
import datetime

class Image(env.db.basemodel):
    chan = ForeignKeyField(schema.Chan, related_name='images')
    name = TextField()
    word = TextField()
    image = TextField()
    tiny = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

Image.create_table(True)
