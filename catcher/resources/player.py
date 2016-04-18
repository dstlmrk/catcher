#!/usr/bin/python
# coding=utf-8

from catcher.api.resource import Collection, Item
from catcher import models as m
from catcher.api.privileges import Privilege
import falcon
import peewee as pw

class Player(Item):

    @falcon.before(Privilege(["club", "admin"]))
    def on_put(self, req, resp, id):
        Privilege.checkClub(req.context['user'], req.context['data'].get('clubId'))
        super(Player, self).on_put(req, resp, id, ['firstname', 'lastname', 'nickname', 'number'])

    @falcon.before(Privilege(["admin"]))
    def on_delete(self, req, resp, id):
        super(Player, self).on_delete(req, resp, id)

class Players(Collection):
    
    @falcon.before(Privilege(["club", "admin"]))
    def on_post(self, req, resp):
        Privilege.checkClub(req.context['user'], req.context['data'].get('clubId'))
        super(Players, self).on_post(req, resp)