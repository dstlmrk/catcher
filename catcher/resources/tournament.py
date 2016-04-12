#!/usr/bin/python
# coding=utf-8

from catcher.api.resource import Collection, Item
from catcher import models as m
from catcher.resources.tournamentCreater import TournamentCreater
import falcon
import logging
import datetime

from catcher.models.queries import Queries

class Tournament(Item):

    @m.db.atomic()
    def prepareTournament(self, id):
        tournament = m.Tournament.\
            select(m.Tournament.teams, m.Tournament.ready).\
            where(m.Tournament.id == id).get()

        if tournament.ready:
            raise ValueError("Tournament %s is already ready" % id)

        teams = m.TeamAtTournament.select().\
            where(m.TeamAtTournament.tournamentId == id).dicts()

        if len(teams) != tournament.teams:
            raise Exception(
                "Tournament has different number of teams"
                " in contrast to TeamAtTournament" % matchId
                )

        # ready Tournament
        m.Tournament.update(ready=True).where(m.Tournament.id==id).execute()

        # Standing
        for x in range(1, len(teams)+1):
             m.Standing.insert(
                tournamentId = id,
                standing = x
                ).execute()

        # Matches
        teamsAdSeeding = {}
        for team in teams:
            teamsAdSeeding[team['seeding']] = team['teamId']

        matches = m.Match.select().\
            where(
                m.Match.tournamentId == 1 and \
                (m.Match.homeSeed != None or m.Match.awaySeed != None) 
                )

        for match in matches:
            m.Match.update(
                homeTeamId = teamsAdSeeding[match.homeSeed],
                awayTeamId = teamsAdSeeding[match.awaySeed]
                ).\
                where(m.Match.id == match.id).execute()

    @m.db.atomic()    
    def terminateTournament(self, id):
        logging.warning("Tournament.terminateTournament() neni implementovano")

    def on_put(self, req, resp, id):
        requestBody = req.context['data']

        tournament = m.Tournament.select(m.Tournament).where(m.Tournament.id==id).get()

        super(Tournament, self).on_put(req, resp, id,
            ['active', 'name', 'startDate', 'endDate', 'city', 'country', 'caldTournamentId']
            )

        edited = False
        if tournament.ready is False and requestBody.get('ready') is True:
            self.prepareTournament(id)
            edited = True

        if tournament.terminated is False and requestBody.get('terminated') is True:
            self.terminateTournament(id)
            edited = True

        if edited:
            resp.status = falcon.HTTP_200 


class Tournaments(Collection):
    
    def on_post(self, req, resp):
        tournamentCreater = TournamentCreater()
        createdTurnament = tournamentCreater.createTournament(req, resp)
        req.context['result'] = createdTurnament 
        resp.status = falcon.HTTP_201


class TournamentStandings(object):

    def on_get(self, req, resp, id):
        tournament = m.Tournament.select(m.Tournament.ready, m.Tournament.terminated).where(m.Tournament.id==id).get()
        if not tournament.ready and not tournament.terminated:
            raise ValueError("Tournament hasn't any standings")
        qr = m.Standing.select().where(m.Standing.tournament==id)
        standings = []
        for standing in qr:
            standings.append(standing.json)
        collection = {
            'teams'     : len(standings),
            'standings' : standings,
            'spirit'    : "UNFINISHED"
            }
        req.context['result'] = collection

class TournamentTeams(object):

    def on_get(self, req, resp, id):
        teams = Queries.getTeams(id)
        collection = {
            'count' : len(teams),
            'items' : teams
        }
        req.context['result'] = collection

    def on_put(self, req, resp, id):
        tournament = m.Tournament.get(id=id)
        if tournament.ready:
            raise ValueError("Tournament is ready and teams can't be changed")
        data = req.context['data']
        qr = m.TeamAtTournament.\
            update(
                teamId = data['teamId']
                ).\
            where(
                m.TeamAtTournament.tournamentId == id,
                m.TeamAtTournament.seeding == data['seeding']
            ).execute()
        resp.status = falcon.HTTP_200 if qr else falcon.HTTP_304
        
        req.context['result'] =  m.TeamAtTournament.get(
            tournamentId = id,
            seeding = data['seeding']
            )

class TournamentMatches(object):

    def on_get(self, req, resp, id):
        matches = Queries.getMatches(
            id,
            req.params.get('matchId'),
            req.params.get('fieldId'),
            req.params.get('date'),
            req.params.get('active'),
            req.params.get('terminated')
            )
        collection = {
            'count'  : len(matches),
            'matches': matches
        }
        req.context['result'] = collection

class TournamentPlayers(object):

    def on_get(self, req, resp, id):
        players = Queries.getPlayers(
            id, req.params.get('teamId'), req.params.get('limit')
            )
        collection = {
            'count': len(players),
            'players': players
        } 
        req.context['result'] = collection

    def on_post(self, req, resp, id):
        newPlayer, created = m.PlayerAtTournament.create_or_get(
            tournamentId = int(id),
            teamId       = req.context['data']['teamId'],
            playerId     = req.context['data']['playerId']
            )
        resp.status = falcon.HTTP_201 if created else falcon.HTTP_200
        req.context['result'] = newPlayer

    def on_delete(self, req, resp, id):
        teamId   = req.context['data'].get('teamId')
        playerId = req.context['data'].get('playerId')
        
        matches = m.PlayerAtTournament.get(
            m.PlayerAtTournament.tournamentId == id,
            m.PlayerAtTournament.teamId       == teamId,
            m.PlayerAtTournament.playerId     == playerId
            ).matches

        if matches == 0:
            d = m.PlayerAtTournament.delete().where(
                m.PlayerAtTournament.tournamentId == id,
                m.PlayerAtTournament.teamId       == teamId,
                m.PlayerAtTournament.playerId     == playerId
                ).execute()
        else:
            raise ValueError("Player has played matches")

class TournamentGroups(object):
    pass