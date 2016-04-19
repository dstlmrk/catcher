#!/usr/bin/python
# coding=utf-8

from catcher.api.resource import Collection, Item
from catcher import models as m
import peewee as pw
from catcher.models.queries import Queries
from catcher.api.privileges import Privilege
import falcon

class Club(Item):

    def on_get(self, req, resp, id):
        req.context['result'] = Queries.getClubs(id)[0]

    @falcon.before(Privilege(["club", "admin"]))
    def on_put(self, req, resp, id):
        Privilege.checkClub(req.context['user'], int(id))
        super(Club, self).on_put(req, resp, id, ['shortcut', 'city', 'country'])
        req.context['result'] = Queries.getClubs(id)[0]

    @falcon.before(Privilege(["admin"]))
    def on_delete(self, req, resp, id):
        super(Club, self).on_delete(req, resp, id)

class Clubs(Collection):

    def on_get(self, req, resp):
        clubs = Queries.getClubs()
        collection = {
            'count' : len(clubs),
            'items' : clubs
        }
        req.context['result'] = collection

    @falcon.before(Privilege(["admin"]))
    def on_post(self, req, resp):
        super(Clubs, self).on_post(req, resp)

class ClubPlayers():

    def on_get(self, req, resp, id):
        qr = m.Player.select().where(m.Player.clubId==id).order_by(m.Player.ranking.desc())
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
                'clubId'   : player.clubId
            })

        collection = {
            'count' : len(players),
            'items' : players
        }

        req.context['result'] = collection

class ClubTeams():

    def on_get(self, req, resp, id):
        q = ("SELECT team.id, team.degree, division.division, division.id, club.name" +
             " FROM team JOIN division ON team.division_id = division.id" +
             " JOIN club ON club.id = team.club_id" +
             " WHERE team.club_id = %s;" % (id))
        qr = m.db.execute_sql(q)
        teams = []
        for row in qr:
            teams.append({
                    'id'         : row[0],
                    'degree'     : row[1],
                    'division'   : {
                        'division' : row[2],
                        'id'       : row[3],
                        },
                    'clubId'     : id,
                    'name'       : (row[4] + " " + row[1])
                })

        collection = {
            'count' : len(teams),
            'items' : teams
        }

        req.context['result'] = collection