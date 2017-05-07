#!/usr/bin/env python2
#-*- coding: utf8 -*-

import datetime

from peewee import *

from taemin import database, schema

class Quotation(database.db.basemodel):
    chan = ForeignKeyField(schema.Chan, related_name='quotes')
    user = ForeignKeyField(schema.User, related_name='quotes')
    value = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

Quotation.create_table(True)
