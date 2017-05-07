#!/usr/bin/env python2
#-*- coding: utf8 -*-

import datetime
from peewee import *

from taemin import schema
from taemin import database

class Savedthings(database.db.basemodel):
    user = ForeignKeyField(schema.User, related_name='savedthings')
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

Savedthings.create_table(True)
