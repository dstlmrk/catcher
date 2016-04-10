#!/usr/bin/python
# coding=utf-8

from catcher import models as m
import falcon

from catcher.resources import Queries

class Points(object):

    def getPoints(self, matchId, order = None):
        '''returns all points from the match'''
        whereOrder = "" if order is None else ("AND point.order = %s" % order) 
        q = ("SELECT match_id, point.order, assist_player_id, score_player_id,"
             " home_score, away_score, home_point, callahan FROM point"
             " WHERE match_id = %s %s ORDER BY point.order DESC;"
             % (matchId, whereOrder))
        qr = m.db.execute_sql(q)
        points = []
        for row in qr:
            points.append({
                'matchId'       : row[0],       
                'order'         : row[1],
                'assistPlayerId': row[2],
                'scorePlayerId' : row[3],
                'homeScore'     : row[4],
                'awayScore'     : row[5],
                'homePoint'     : row[6],
                'callahan'      : row[7]
                })
        return points

    def getPlayersTeamId(self, tournamentId, teamId):
        '''returns one number'''
        q = ("SELECT team_id FROM player_at_tournament"
             " WHERE tournament_id = %s AND player_id = %s;"
             % (tournamentId, teamId)
             )
        return m.db.execute_sql(q).fetchone()[0]
    
    def getMatch(self, matchId):
        '''returns triple'''
        q = ("SELECT home_team_id, away_team_id, active"
             " FROM catcher.match WHERE id = %s;"
             % (matchId)
             )
        return m.db.execute_sql(q).fetchone()

    def getLastPoint(self, matchId):
        '''returns tripe'''
        q = ("SELECT point.order, home_score, away_score"
             " FROM point WHERE match_id = %s ORDER BY point.order DESC LIMIT 1;"
             % (matchId)
             )
        return m.db.execute_sql(q).fetchone()

    def checkPlayers(self, tournamentId, teamId, assistPlayerId, scorePlayerId, callahan):
        if not callahan and assistPlayerId:
            if assistPlayerId == scorePlayerId:
                raise ValueError("Assisting player and scoring player is the one")
            # assisting player
            hisTeamId = self.getPlayersTeamId(tournamentId, assistPlayerId)
            if hisTeamId != teamId:
                raise ValueError("Team %s hasn't player %s" % (teamId, assistPlayerId))

        if scorePlayerId is not None:
            # scoring player
            hisTeamId = self.getPlayersTeamId(tournamentId, scorePlayerId)
            if hisTeamId != teamId:
                raise ValueError("Team %s hasn't player %s" % (teamId, scorePlayerId))
        return True

    def updateMatchScore(self, matchId, forHome, inc = 1):
        if forHome:
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
                    m.PlayerAtMatch.player == playerId,
                    m.PlayerAtMatch.match  == matchId
                ).execute()
        elif state == 'A':
            m.PlayerAtMatch.update(
                    assists = (m.PlayerAtMatch.assists + inc),
                    total   = (m.PlayerAtMatch.total + inc)
                ).where(
                    m.PlayerAtMatch.player == playerId,
                    m.PlayerAtMatch.match == matchId
                ).execute()


        # TODO: zapocitat celkove statistiky na hrace, ne jenom na zapas


    def on_get(self, req, resp, id, matchId):
        match = Queries.getMatches(id, matchId)[0]
        match['points'] = self.getPoints(matchId)
        req.context['result'] = match

    def on_post(self, req, resp, id, matchId):
        data           = req.context['data']
        assistPlayerId = data.get('assistPlayerId')
        scorePlayerId  = data.get('scorePlayerId')
        callahan       = data.get('callahan', False)
        homePoint      = bool(data['homePoint'])

        homeTeamId, awayTeamId, active = self.getMatch(matchId)

        if not active:
            raise ValueError("Match isn't active")

        if homePoint:
            teamId = homeTeamId
        else:
            teamId = awayTeamId

        self.checkPlayers(id, teamId, assistPlayerId, scorePlayerId, callahan)

        with m.db.transaction():

            if not callahan:
                if assistPlayerId:
                    self.updatePlayerStatistic(id, assistPlayerId, matchId, 'A')
                if scorePlayerId:
                    self.updatePlayerStatistic(id, scorePlayerId, matchId, 'S')

            order, homeScore, awayScore = self.getLastPoint(matchId)
            
            order += 1
            
            if homePoint:
                homeScore += 1
            else:
                awayScore += 1

            m.Point.insert(
                    homePoint      = homePoint,
                    matchId        = matchId,    
                    order          = order,
                    assistPlayerId = assistPlayerId if not callahan else None,
                    scorePlayerId  = scorePlayerId if not callahan else None,
                    homeScore      = homeScore,
                    awayScore      = awayScore,
                    callahan       = callahan
                ).execute()

            self.updateMatchScore(matchId, homePoint)

            point = m.Point.get(matchId=matchId, order=order)

        req.context['result'] = point
        resp.status = falcon.HTTP_201

    def on_put(self, req, resp, id, matchId):
        editableCols   = ['assistPlayerId', 'scorePlayerId', 'callahan']
        data           = req.context['data']
        order          = data['order']
        point          = self.getPoints(matchId, order)[0]
        assistPlayerId = point['assistPlayerId']
        scorePlayerId  = point['scorePlayerId']
        callahan       = data['callahan']

        homeTeamId, awayTeamId, active = self.getMatch(point['matchId'])

        if point['homePoint']:
            teamId = homeTeamId
        else:
            teamId = awayTeamId

        self.checkPlayers(id, teamId, assistPlayerId, scorePlayerId, callahan)

        params = None
        qr     = None
        if editableCols is not None:
            params = { key : data[key] for key in data if key in editableCols}

        with m.db.transaction():
            # delete players statistics, if they are changed
            newAssistPlayerId = data.get('assistPlayerId')
            if assistPlayerId != newAssistPlayerId:
                self.updatePlayerStatistic(id, assistPlayerId, matchId, 'A', (-1))
                self.updatePlayerStatistic(id, newAssistPlayerId, matchId, 'A', 1)
            newScorePlayerId = data.get('scorePlayerId')
            if scorePlayerId != newScorePlayerId:
                self.updatePlayerStatistic(id, scorePlayerId, matchId, 'S', (-1))
                self.updatePlayerStatistic(id, scorePlayerId, matchId, 'S', 1)

            if params:
                qr = m.Point.update(**params).where(
                        m.Point.matchId == matchId,
                        m.Point.order == order
                    ).execute()

        req.context['result'] = m.Point.select().where(
                m.Point.matchId == matchId,
                m.Point.order == order
            ).get()
        resp.status = falcon.HTTP_200 if qr else falcon.HTTP_304

    def on_delete(self, req, resp, id, matchId):
        # TODO: unite this two queries
        order, homeScore, awayScore = self.getLastPoint(matchId)
        point = self.getPoints(matchId, order)[0]
        
        assistPlayerId = point['assistPlayerId']
        scorePlayerId  = point['scorePlayerId']

        with m.db.transaction():
            # delete from match table
            self.updateMatchScore(matchId, point['homePoint'], (-1))
            # delete players statistics
            if assistPlayerId:
                self.updatePlayerStatistic(id, assistPlayerId, matchId, 'A', (-1))
            if scorePlayerId:
                self.updatePlayerStatistic(id, scorePlayerId, matchId, 'S', (-1))
            # delete point
            m.Point.delete().where(
                    m.Point.matchId == matchId,
                    m.Point.order == order
                ).execute()