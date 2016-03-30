#!/usr/bin/python
# coding=utf-8

from api.resource import Collection, Item
import models as m
import falcon
import peewee as pw

class Player(Item):
    pass

class Players(Collection):
    pass

class PlayerAtTournament(object):

    def on_get(self, req, resp, tournamentId, teamId, playerId):
        player = m.PlayerAtTournament.get(
            tournament = tournamentId,
            team       = teamId,
            player     = playerId
        )
        req.context['result'] = player


    def on_post(self, req, resp, tournamentId, teamId, playerId):
        m.Tournament.get(m.Tournament.id == tournamentId).id
        m.Team.get(m.Team.id == teamId).id
        newPlayer, created = m.PlayerAtTournament.create_or_get(
            tournament = tournamentId,
            team       = teamId,
            player     = playerId
        )
        resp.status = falcon.HTTP_201 if created is True else falcon.HTTP_200
        req.context['result'] = newPlayer


    def on_put(self, req, resp, tournamentId, teamId, playerId):
        pass
        # TODO: zde se NEbudou editovat statistiky, to musi byt nekde automaticky

    def on_delete(self, req, resp, tournamentId, teamId, playerId):
        m.PlayerAtTournament.delete().where(
            m.PlayerAtTournament.tournament == tournamentId,
            m.PlayerAtTournament.team       == teamId,
            m.PlayerAtTournament.player     == playerId
        ).execute()