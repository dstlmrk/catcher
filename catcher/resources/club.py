#!/usr/bin/python
# coding=utf-8

# from catcher import api
from api.resource import Collection, Item
import models as m
import peewee as pw
from peewee import JOIN

class Club(Item):

    def on_get(self, req, resp, id):
        qr = m.Club.select(m.Club, m.User).join(m.User, JOIN.LEFT_OUTER).where(m.Club.id==id).get()
        user = {}
        if qr.user.id is not None:
            user = {
                'id'          : qr.user.id,
                'nickname'    : qr.user.nickname,
                'email'       : qr.user.email,
                'createdAt'   : qr.user.createdAt,
                'lastLoginAt' : qr.user.lastLoginAt
            }
        club = {
            'id'      : qr.id,
            'caldId'  : qr.caldId,
            'name'    : qr.name,
            'shortcut': qr.shortcut,
            'city'    : qr.city,
            'country' : qr.country,
            'user'    : user
        }
        req.context['result'] = club

    def on_put(self, req, resp, id):
        super(Club, self).on_put(req, resp, id, ['shortcut', 'city', 'country'])

class Clubs(Collection):
    
    def on_get(self, req, resp):
        q = ("SELECT club.id, club.cald_id, club.name, club.shortcut, club.city, club.country," +
             " user.id, user.nickname, user.email, user.created_at, user.last_login_at"
             " FROM catcher.club LEFT OUTER JOIN user ON user.id = club.user_id")
        qr = m.db.execute_sql(q)
        clubs = []
        for row in qr:
            user = {}
            if row[6] is not None:
                user = {
                    'id'          : row[6],
                    'nickname'    : row[7],
                    'email'       : row[8],
                    'createdAt'   : row[9],
                    'lastLoginAt' : row[10]
                    }
            clubs.append({
                'id'      : row[0],
                'caldId'  : row[1],
                'name'    : row[2],
                'shortcut': row[3],
                'city'    : row[4],
                'country' : row[5],
                'user'    : user
                })

        collection = {
            'count' : len(clubs),
            'clubs' : clubs
        }

        req.context['result'] = collection

class ClubPlayers():

    def on_get(self, req, resp, id):
        qr = m.Player.select().where(m.Player.club==id).order_by(m.Player.ranking.desc())
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
            'count' : len(players),
            'players' : players
        }

        req.context['result'] = collection

class ClubTeams():

    def on_get(self, req, resp, id):
        q = ("SELECT team.id, team.degree, division.division, division.id, club.name" +
             " FROM catcher.team JOIN division ON team.division_id = division.id" +
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
            'teams' : teams
        }

        req.context['result'] = collection