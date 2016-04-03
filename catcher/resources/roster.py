#!/usr/bin/python
# coding=utf-8

import models as m
import falcon

class Rosters(object):

    def on_post(self, req, resp, id):
        data = req.context.get('data')
        if not data:
            raise ValueError("Request body is empty")
        m.Tournament.get(m.Tournament.id == id).id
        m.Team.get(m.Team.id == data.get('teamId')).id
        m.Player.get(m.Player.id == data.get('playerId')).id

        newPlayer, created = m.PlayerAtTournament.create_or_get(
            tournament = id,
            team       = data.get('teamId'),
            player     = data.get('playerId')
        )
        resp.status = falcon.HTTP_201 if created is True else falcon.HTTP_200
        print resp.status
        req.context['result'] = newPlayer
       
    def on_delete(self, req, resp, id):
        data = req.context.get('data')
        if not data:
            raise ValueError("Request body is empty")
        m.Tournament.get(m.Tournament.id == id).id
        m.Team.get(m.Team.id == data.get('teamId')).id
        m.Player.get(m.Player.id == data.get('playerId')).id

        m.PlayerAtTournament.delete().where(
            m.PlayerAtTournament.tournament == id,
            m.PlayerAtTournament.team       == data.get('teamId'),
            m.PlayerAtTournament.player     == data.get('playerId')
        ).execute()