#!/usr/bin/python
# coding=utf-8

import models as m
import falcon

class Points(object):

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
    
    def on_post(self, req, resp, id):
        data           = req.context['data']
        assistPlayerId = data.get('assistPlayerId')
        scorePlayerId  = data.get('scorePlayerId')
        callahan       = data.get('callahan', False)
        matchId        = data['matchId']
        homePoint      = bool(data['homePoint'])

        homeTeamId, awayTeamId, active = self.getMatch(matchId)

        if not active:
            raise ValueError("Match isn't active")

        if homePoint:
            teamId = homeTeamId
        else:
            teamId = awayTeamId

        if not callahan and assistPlayerId:
            if assistPlayerId == scorePlayerId:
                raise ValueError("Assisting player and scoring player is the one")
            # assisting player
            hisTeamId = self.getPlayersTeamId(id, assistPlayerId)
            if hisTeamId != teamId:
                raise ValueError("Team %s hasn't player %s" % (teamId, assistPlayerId))

        if scorePlayerId is not None:
            # scoring player
            hisTeamId = self.getPlayersTeamId(id, scorePlayerId)
            if hisTeamId != teamId:
                raise ValueError("Team %s hasn't player %s" % (teamId, scorePlayerId))

        with m.db.transaction():

            # player at match table -------------------------------
            if assistPlayerId:
                m.PlayerAtMatch.update(
                        assists = (m.PlayerAtMatch.assists + 1),
                        total   = (m.PlayerAtMatch.total + 1)
                    ).where(
                        m.PlayerAtMatch.player == assistPlayerId,
                        m.PlayerAtMatch.match == matchId
                    ).execute()

            if scorePlayerId:
                m.PlayerAtMatch.update(
                        scores = (m.PlayerAtMatch.scores + 1),
                        total  = (m.PlayerAtMatch.total + 1)
                    ).where(
                        m.PlayerAtMatch.player == scorePlayerId,
                        m.PlayerAtMatch.match == matchId
                    ).execute()
            # -------------------------------------------------------
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
                    assistPlayerId = assistPlayerId,
                    scorePlayerId  = scorePlayerId,
                    homeScore      = homeScore,
                    awayScore      = awayScore,
                    callahan       = callahan
                ).execute()

            m.Match.update(
                    homeScore = homeScore,
                    awayScore = awayScore
                ).where(
                    m.Match.id == matchId
                ).execute()

            point = m.Point.get(matchId=matchId, order=order)

        req.context['result'] = point
        resp.status = falcon.HTTP_201