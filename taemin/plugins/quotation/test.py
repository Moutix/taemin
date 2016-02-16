#!/usr/bin/env python2
# -*- coding: utf8 -*-

from taemin import env, schema
from quotation_schema import Quotation
import re
from peewee import fn

def main():
    chan = "#miku"
    msg = "add Ningirsu 3"
    kws = re.search('(\w+)\s(\w+)\s(\d+)', msg)
    quote_key = kws.group(1)
    quote_user = kws.group(2)
    quote_limit = int(kws.group(3))
    print quote_key, quote_user, quote_limit
    1/0
    if quote_key == "add":
        user = schema.User.get(schema.User.name % quote_user)
        chan = schema.Chan.get(schema.Chan.name % chan)
        print user.name
        print chan.name
        quote = schema.Message.select().where((schema.Message.user == user) & (schema.Message.chan == chan)).order_by(schema.Message.created_at.desc()).limit(quote_limit).get()
        print quote.message
        quotes = [quote for quote in schema.Message.select().where((schema.Message.user == user) & (schema.Message.chan == chan)).order_by(schema.Message.created_at.desc()).offset(quote_limit - 1).limit(1)]
        print quotes

if __name__ == "__main__":
    main()
