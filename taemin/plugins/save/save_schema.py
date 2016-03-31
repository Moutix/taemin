#!/usr/bin/env python2
#-*- coding: utf8 -*-

from taemin import database, schema
from peewee import *
import datetime

class Savedthings(database.db.basemodel):
    user = ForeignKeyField(schema.User, related_name='savedthings')
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

Savedthings.create_table(True)
