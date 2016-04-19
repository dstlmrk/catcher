#!/usr/bin/python
# coding=utf-8

from catcher.api.resource import Collection, Item
from catcher import models as m
from catcher.models.queries import Queries
from catcher.api.privileges import Privilege
import falcon

import logging

class Match(Item):

    @staticmethod
    def updateStanding(tournamentId, teamId, standing):
        m.Standing.update(teamId = teamId).where(
            m.Standing.standing == standing,
            m.Standing.tournamentId == tournamentId
            ).execute()

    @staticmethod
    def addTeamInNextStep(tournamentId, teamId, idId):
        identificator = m.Identificator.get(id = idId)
        match = m.Match.get(tournamentId=tournamentId, identificatorId=idId)

        if identificator.matchId:
            logging.info("4: Saving team in match %s" % identificator.identificator)
            # doplnim do dalsiho zapasu
            if match.homeTeamId is None:
                logging.info("5: Team will play as home")
                match.homeTeamId = teamId
            elif match.awayTeamId is None:
                logging.info("5: Team will play as away")
                match.awayTeamId = teamId
            else:
                raise RuntimeError("In the match %s want to be more than two teams" % idId)
        else:
            logging.info(
                "4: Saving team in group %s"
                % identificator.identificator
                )
            # TODO: continue in group

        match.save()

    @m.db.atomic()
    def activeMatch(self, matchId):
        
        match = m.Match.get(id=matchId)

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

        # TODO: vsem hracum pridelat jednicku v total PlayerAtTournament a otestovat

        match.homeScore = 0
        match.awayScore = 0
        match.active = True
        match.save()

    @m.db.atomic()
    def terminateMatch(self, matchId):
        logging.info("1: Match %s is in terminating" % matchId)

        match = m.Match.get(id=matchId)

        # if match has next step, there have to be winner (playoff)
        if match.looserFinalStanding or match.winnerFinalStanding \
        or match.winnerNextStepId or match.looserNextStepId:
            if match.homeScore > match.awayScore:
                logging.info("2: Home team won: %s vs %s" % (match.homeTeamId, match.awayTeamId))
                winnerTeamId = match.homeTeamId
                looserTeamid = match.awayTeamId
            elif match.homeScore < match.awayScore:
                logging.info("2: Away team won: %s vs %s" % (match.homeTeamId, match.awayTeamId))
                winnerTeamId = match.awayTeamId
                looserTeamid = match.homeTeamId
            else:
                raise ValueError("Match have to have the one winner")

            if match.winnerFinalStanding:
                logging.info("3: Winner ends on %s. place" % match.winnerFinalStanding)
                Match.updateStanding(match.tournamentId, winnerTeamId, match.winnerFinalStanding)
            if match.winnerNextStepId:
                identificator = m.Identificator.get(id = match.winnerNextStepId)
                logging.info(
                    "3: Winner's next match is %s (%s)" 
                    % (identificator.matchId, identificator.identificator)
                    )
                Match.addTeamInNextStep(match.tournamentId, winnerTeamId, match.winnerNextStepId)

            if match.looserFinalStanding:
                logging.info("3: Looser ends on %s. place" % match.looserFinalStanding)
                Match.updateStanding(match.tournamentId, looserTeamid, match.looserFinalStanding)
            if match.looserNextStepId:
                identificator = m.Identificator.get(id = match.looserNextStepId)
                logging.info(
                    "3: Looser's next match is %s (%s)" 
                    % (identificator.matchId, identificator.identificator)
                    )
                Match.addTeamInNextStep(match.tournamentId, looserTeamid, match.looserNextStepId)
        else:
            pass
            # TODO: Match hasn't next step, so it's in a group probably.
            # I can identify group by idendificator. 

        match.terminated = True
        match.save()
        # now is allowed consigning Spirit of the Game

    def on_get(self, req, resp, id):
        req.context['result'] = Queries.getMatches(matchId=id)[0]

    @falcon.before(Privilege(["organizer", "admin"]))
    def on_put(self, req, resp, id):
        match = m.Match.get(id=id)
        Privilege.checkOrganizer(req.context['user'], match.tournamentId)
        data = req.context['data']

        super(Match, self).on_put(req, resp, id,
            ['fieldId', 'startTime', 'endTime', 'description']
            )
        
        edited = False
        if not match.active and data.get('active'):
            self.activeMatch(id)
            edited = True

        if match.active and not match.terminated and data.get('terminated'):
            self.terminateMatch(id)
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

    @falcon.before(Privilege(["organizer", "admin"]))
    def on_post(self, req, resp, id):
        match = m.Match.get(id=id)
        Privilege.checkOrganizer(req.context['user'], match.tournamentId)

        data           = req.context['data']
        assistPlayerId = data.get('assistPlayerId')
        scorePlayerId  = data.get('scorePlayerId')
        callahan       = data.get('callahan', False)
        homePoint      = bool(data['homePoint'])
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

    @falcon.before(Privilege(["organizer", "admin"]))
    def on_delete(self, req, resp, id):
        match          = m.Match.get(id=id)
        Privilege.checkOrganizer(req.context['user'], match.tournamentId)
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

    @falcon.before(Privilege(["organizer", "admin"]))
    def on_put(self, req, resp, id, order):
        match          = m.Match.get(id=id)
        Privilege.checkOrganizer(req.context['user'], match.tournamentId)

        editableCols   = ['assistPlayerId', 'scorePlayerId', 'callahan']
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