#!/usr/bin/python
# coding=utf-8

from api.resource import Collection, Item
import models as m
import falcon
import peewee as pw

class Player(Item):

    def on_get(self, req, resp, id):
        qr = m.Player.select(m.Player).where(m.Player.id==id).get()
        player = {
            'id'       : qr.id,
            'firstname': qr.firstname,
            'lastname' : qr.lastname,
            'nickname' : qr.nickname,
            'number'   : qr.number,
            'ranking'  : qr.ranking,
            'caldId'   : qr.caldId,
            'clubId'   : qr.club_id
        }
        req.context['result'] = player

    def on_put(self, req, resp, id):
        super(Player, self).on_put(req, resp, id, ['firstname', 'lastname', 'nickname', 'number'])

class Players(Collection):

    def on_get(self, req, resp):
        qr = m.Player.select(m.Player)
        players = []
        for player in qr:
            players.append({
                'id'       : player.id,
                'firstname': player.firstname,
                'lastname' : player.lastname,
                'nickname' : player.nickname,
                'number'   : player.number,
                'ranking'  : player.ranking,
                'caldId'   : player.caldId,
                'clubId'   : player.club_id
                })

        collection = {
            'count'   : len(players),
            'players' : players
        }

        req.context['result'] = collection
