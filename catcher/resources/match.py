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
    def addTeamInNextStep(tournamentId, teamId, ide):
        identificator = m.Identificator.get(ide = ide)
        match = m.Match.get(tournamentId=tournamentId, ide=ide)

        if identificator.matchId:
            logging.info("4: Saving team in match %s" % identificator.ide)
            # doplnim do dalsiho zapasu
            if match.homeTeamId is None:
                logging.info("5: Team will play as home")
                match.homeTeamId = teamId
            elif match.awayTeamId is None:
                logging.info("5: Team will play as away")
                match.awayTeamId = teamId
            else:
                raise RuntimeError("In the match %s want to be more than two teams" % ide)
        else:
            logging.info(
                "4: Saving team in group %s"
                % identificator.ide
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

    def updateGroupTable(self, winner, looser, winnerScore, looserScore):
        winner.matches      = winner.matches + 1
        winner.wins         = winner.wins + 1
        winner.plus         = winner.plus + winnerScore
        winner.minus        = winner.minus + looserScore
        winner.points       = winner.points + 2
        looser.matches      = looser.matches + 1
        looser.losses       = looser.losses + 1
        looser.plus         = looser.plus + looserScore
        looser.minus        = looser.minus + winnerScore
        winner.save()
        looser.save()

    def recomputeGroup(self, tournamentId, groupIde):
        # prepocitat vysledky
        # teams = []

        teams = m.GroupHasTeam.select().where(
            m.GroupHasTeam.tournamentId == tournamentId,
            m.GroupHasTeam.ide == groupIde
            ).order_by(
            m.GroupHasTeam.points.desc(),
            (m.GroupHasTeam.plus).desc()
            )

        standing = 1
        for team in teams:
            team.standing = standing
            team.save()
            standing += 1
            print team


        matches = m.Match.select().where(
            m.Match.groupIde == groupIde
            )
        for match in matches:
            print match
            if not match.terminated:
                return

        logging.info("Group is complete")

        for team in teams:
            advancement = m.Advancement.get(
                tournamentId = tournamentId,
                ide = groupIde,
                standing = team.standing
                )

            if advancement.finalStanding:
                Match.updateStanding(
                    tournamentId, team.teamId, advancement.finalStanding
                    )
            elif advancement.nextStepIde:
                Match.addTeamInNextStep(
                    tournamentId, team.teamId, advancement.nextStepIde
                    )
            else:
                raise RuntimeError(
                    "Team %s doesn't know, where continue from %s group"
                    % (team.teamId, groupIde)
                    )



    @m.db.atomic()
    def terminateMatch(self, matchId):
        logging.info("1: Match %s is in terminating" % matchId)

        match = m.Match.get(id=matchId)
        match.terminated = True
        match.save()

        if match.homeScore > match.awayScore:
            logging.info("2: Home team won: %s vs %s" % (match.homeTeamId, match.awayTeamId))
            winnerTeamId = match.homeTeamId
            winnerScore  = match.homeScore
            looserTeamId = match.awayTeamId
            looserScore  = match.awayScore
        elif match.homeScore < match.awayScore:
            logging.info("2: Away team won: %s vs %s" % (match.homeTeamId, match.awayTeamId))
            winnerTeamId = match.awayTeamId
            winnerScore  = match.awayScore
            looserTeamId = match.homeTeamId
            looserScore  = match.homeScore
        else:
            raise ValueError("Match have to have the one winner")

        # if match has next step, there have to be winner (playoff)
        if not match.groupIde:
            if match.winnerFinalStanding:
                logging.info("3: Winner ends on %s. place" % match.winnerFinalStanding)
                Match.updateStanding(match.tournamentId, winnerTeamId, match.winnerFinalStanding)
            if match.winnerNextStepIde:
                identificator = m.Identificator.get(ide = match.winnerNextStepIde)
                logging.info(
                    "3: Winner's next match is %s (%s)" 
                    % (identificator.matchId, identificator.ide)
                    )
                Match.addTeamInNextStep(match.tournamentId, winnerTeamId, match.winnerNextStepIde)

            if match.looserFinalStanding:
                logging.info("3: Looser ends on %s. place" % match.looserFinalStanding)
                Match.updateStanding(match.tournamentId, looserTeamId, match.looserFinalStanding)
            if match.looserNextStepIde:
                identificator = m.Identificator.get(ide = match.looserNextStepIde)
                logging.info(
                    "3: Looser's next match is %s (%s)" 
                    % (identificator.matchId, identificator.ide)
                    )
                Match.addTeamInNextStep(match.tournamentId, looserTeamId, match.looserNextStepIde)
        else:
            print match.homeScore, match.awayScore

            winner = m.GroupHasTeam.get(
                tournamentId = match.tournamentId,
                ide = match.groupIde,
                teamId = winnerTeamId
                )

            looser = m.GroupHasTeam.get(
                tournamentId = match.tournamentId,
                ide = match.groupIde,
                teamId = looserTeamId
                )

            self.updateGroupTable(winner, looser, winnerScore, looserScore)

            self.recomputeGroup(match.tournamentId, match.groupIde)

        # now is allowed consigning Spirit of the Game

    def on_get(self, req, resp, id):
        req.context['result'] = Queries.getMatches(matchId=id)[0]

    @falcon.before(Privilege(["organizer", "admin"]))
    def on_put(self, req, resp, id):
        match = m.Match.get(id=id)
        Privilege.checkOrganizer(req.context['user'], match.tournamentId)
        data = req.context['data']


        tournament = m.Tournament.get(id=match.tournamentId)
        
        activated = False
        if not match.active and data.get('active'):
            if not tournament.ready:
                raise ValueError("Tournament is not ready yet")

            self.activeMatch(id)
            activated = True

        # after active, because it rewrites score
        super(Match, self).on_put(req, resp, id,
            ['homeScore', 'awayScore', 'fieldId', 'startTime', 'endTime', 'description']
            )

        if 'homeScore' in data and 'awayScore' in data:
            pass
            # TODO: pri zmene skore smazat vsechny doposud odehrane body

        terminated = False
        if (match.active or activated) and not match.terminated and data.get('terminated'):
            self.terminateMatch(id)
            terminated = True

        if activated or terminated:
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

            point = Queries.getPoints(
                matchId=match.id, order=order
                )[0]

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