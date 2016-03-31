#!/usr/bin/env python2
#-*- coding: utf8 -*-

from taemin import database, schema
from peewee import *
import datetime

class Shifumi(database.db.basemodel):
    user = ForeignKeyField(schema.User, related_name='shifumis')
    my_value = TextField()
    user_value = TextField()
    winner = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

Shifumi.create_table(True)
