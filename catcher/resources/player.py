#!/usr/bin/python
# coding=utf-8

from catcher.api.resource import Collection, Item
from catcher import models as m
import falcon
import peewee as pw

class Player(Item):

    def on_put(self, req, resp, id):
        super(Player, self).on_put(req, resp, id, ['firstname', 'lastname', 'nickname', 'number'])

class Players(Collection):
    pass