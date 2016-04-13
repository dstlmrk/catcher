#!/usr/bin/python
# coding=utf-8

from catcher.api.resource import Collection, Item
from catcher import models as m
from catcher.models.queries import Queries
import falcon

class Match(Item):

    def activeMatch(self, matchId):
        
        match = m.Match.get(id=matchId)
        match.homeScore = 0
        match.awayScore = 0
        match.save()

        # fill in tables with players per match 
        homeTeamPlayers = m.PlayerAtTournament.select().where(
                m.PlayerAtTournament.tournamentId == match.tournamentId,
                m.PlayerAtTournament.teamId       == match.homeTeamId
            )
        for player in homeTeamPlayers:
            m.PlayerAtMatch.insert(
                matchId  = matchId,
                playerId = player.playerId
                ).execute()
        awayTeamPlayers = m.PlayerAtTournament.select().where(
                m.PlayerAtTournament.tournamentId == match.tournamentId,
                m.PlayerAtTournament.teamId       == match.awayTeamId
            )
        for player in awayTeamPlayers:
            m.PlayerAtMatch.insert(
                matchId  = matchId,
                playerId = player.playerId
                ).execute()

    def on_get(self, req, resp, id):
        req.context['result'] = Queries.getMatches(matchId=id)[0]

    def on_put(self, req, resp, id):
        data = req.context['data']
        match = m.Match.get(id=id)
        super(Match, self).on_put(req, resp, id,
            ['active', 'fieldId', 'startTime', 'endTime', 'terminated', 'description']
            )
        
        edited = False
        if match.active is False and data.get('active') is True:
            self.activeMatch(id)
            edited = True

        if edited:
            resp.status = falcon.HTTP_200 

        req.context['result'] = Queries.getMatches(matchId = id)[0]


class Point(object):

    def checkPlayers(self, tournamentId, teamId, assistPlayerId, scorePlayerId, callahan):
        if not callahan and assistPlayerId:
            if assistPlayerId == scorePlayerId:
                raise ValueError("Assisting player and scoring player is the one")
            # assisting player
            hisTeamId = Queries.getPlayersTeamId(tournamentId, assistPlayerId)
            if hisTeamId != teamId:
                raise ValueError("Team %s hasn't player %s" % (teamId, assistPlayerId))

        if scorePlayerId is not None:
            # scoring player
            hisTeamId = Queries.getPlayersTeamId(tournamentId, scorePlayerId)
            if hisTeamId != teamId:
                raise ValueError("Team %s hasn't player %s" % (teamId, scorePlayerId))
        return True

    def updateMatchScore(self, matchId, homePoint, inc = 1):
        if homePoint:
            m.Match.update(
                    homeScore = (m.Match.homeScore + inc)
                ).where(
                    m.Match.id == matchId
                ).execute()
        else:
            m.Match.update(
                    awayScore = (m.Match.awayScore + inc)
                ).where(
                    m.Match.id == matchId
                ).execute()

    def updatePlayerStatistic(self, tournamentId, playerId, matchId, state, inc = 1):
        if state == 'S':
            m.PlayerAtMatch.update(
                    scores = (m.PlayerAtMatch.scores + inc),
                    total  = (m.PlayerAtMatch.total + inc)
                ).where(
                    m.PlayerAtMatch.playerId == playerId,
                    m.PlayerAtMatch.matchId  == matchId
                ).execute()

            m.PlayerAtTournament.update(
                    scores = (m.PlayerAtTournament.scores + inc),
                    total  = (m.PlayerAtTournament.total + inc)
                ).where(
                    m.PlayerAtTournament.playerId == playerId,
                    m.PlayerAtTournament.tournamentId  == tournamentId
                ).execute()

        elif state == 'A':
            m.PlayerAtMatch.update(
                    assists = (m.PlayerAtMatch.assists + inc),
                    total   = (m.PlayerAtMatch.total + inc)
                ).where(
                    m.PlayerAtMatch.playerId == playerId,
                    m.PlayerAtMatch.matchId  == matchId
                ).execute()

            m.PlayerAtTournament.update(
                    assists = (m.PlayerAtTournament.assists + inc),
                    total   = (m.PlayerAtTournament.total + inc)
                ).where(
                    m.PlayerAtTournament.playerId == playerId,
                    m.PlayerAtTournament.tournamentId  == tournamentId
                ).execute()


class MatchPoints(Point):

    def on_get(self, req, resp, id):
        match = Queries.getMatches(matchId=id)[0]
        match['points'] = Queries.getPoints(id)
        req.context['result'] = match

    def on_post(self, req, resp, id):
        data           = req.context['data']
        assistPlayerId = data.get('assistPlayerId')
        scorePlayerId  = data.get('scorePlayerId')
        callahan       = data.get('callahan', False)
        homePoint      = bool(data['homePoint'])
        match          = m.Match.get(id=id)
        tournament     = m.Tournament.get(id=match.tournamentId)

        if not tournament.ready:
            raise ValueError("Tournament isn't ready")

        if not match.active:
            raise ValueError("Match isn't active")

        teamId = match.homeTeamId if homePoint else match.awayTeamId

        self.checkPlayers(match.tournamentId, teamId, assistPlayerId, scorePlayerId, callahan)
        with m.db.transaction():

            if not callahan:
                if assistPlayerId:
                    self.updatePlayerStatistic(
                        match.tournamentId, assistPlayerId, match.id, 'A'
                        )
            if scorePlayerId:
                self.updatePlayerStatistic(
                    match.tournamentId, scorePlayerId, match.id, 'S'
                    )

            order, homeScore, awayScore = Queries.getLastPoint(match.id)
            
            order += 1
            
            if homePoint:
                homeScore += 1
            else:
                awayScore += 1

            m.Point.insert(
                    homePoint      = homePoint,
                    matchId        = match.id,    
                    order          = order,
                    assistPlayerId = assistPlayerId if not callahan else None,
                    scorePlayerId  = scorePlayerId if not callahan else None,
                    homeScore      = homeScore,
                    awayScore      = awayScore,
                    callahan       = callahan
                ).execute()

            self.updateMatchScore(match.id, homePoint)

            point = m.Point.get(matchId=match.id, order=order)

        req.context['result'] = point
        resp.status = falcon.HTTP_201

    def on_delete(self, req, resp, id):
        match          = m.Match.get(id=id)
        # TODO: unite this two queries
        order, homeScore, awayScore = Queries.getLastPoint(match.id)
        point = Queries.getPoints(match.id, order)[0]
        
        assistPlayerId = point['assistPlayer']['id']
        scorePlayerId  = point['scorePlayer']['id']

        with m.db.transaction():
            # delete from match table
            self.updateMatchScore(match.id, point['homePoint'], (-1))
            # delete players statistics
            if assistPlayerId:
                self.updatePlayerStatistic(match.tournamentId, assistPlayerId, match.id, 'A', (-1))
            if scorePlayerId:
                self.updatePlayerStatistic(match.tournamentId, scorePlayerId, match.id, 'S', (-1))
            # delete point
            m.Point.delete().where(
                    m.Point.matchId == match.id,
                    m.Point.order == order
                ).execute()

class MatchPoint(Point):

    def on_put(self, req, resp, id, order):
        
        editableCols   = ['assistPlayerId', 'scorePlayerId', 'callahan']
        match          = m.Match.get(id=id)
        point          = m.Point.get(matchId=match.id, order=order)
        data           = req.context['data']
        assistPlayerId = data.get('assistPlayerId')
        scorePlayerId  = data.get('scorePlayerId')
        callahan       = data.get('callahan', False)

        teamId = match.homeTeamId if point.homePoint else match.awayTeamId

        self.checkPlayers(match.tournamentId, teamId, assistPlayerId, scorePlayerId, callahan)

        params = None
        qr     = None
        if editableCols is not None:
            params = { key : data[key] for key in data if key in editableCols}
            if callahan and 'assistPlayerId' in params:
                del params['assistPlayerId']

        with m.db.transaction():
            # delete players statistics, if they are changed
            if callahan:
                self.updatePlayerStatistic(match.tournamentId, point.assistPlayerId, match.id, 'A', (-1))

            if assistPlayerId and point.assistPlayerId != assistPlayerId and not callahan:
                self.updatePlayerStatistic(match.tournamentId, point.assistPlayerId, match.id, 'A', (-1))
                self.updatePlayerStatistic(match.tournamentId, assistPlayerId, match.id, 'A', 1)
        
            if scorePlayerId and point.scorePlayerId != scorePlayerId:
                self.updatePlayerStatistic(match.tournamentId, point.scorePlayerId, match.id, 'S', (-1))
                self.updatePlayerStatistic(match.tournamentId, scorePlayerId, match.id, 'S', 1)

            if params:
                qr = m.Point.update(**params).where(
                        m.Point.matchId == match.id,
                        m.Point.order == order
                    ).execute()

        req.context['result'] = m.Point.select().where(
                m.Point.matchId == match.id,
                m.Point.order == order
            ).get()
        resp.status = falcon.HTTP_200 if qr else falcon.HTTP_304