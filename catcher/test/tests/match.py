#!/usr/bin/python
# coding=utf-8

from falcon import HTTP_200, HTTP_201, HTTP_400
from tournament import TournamentTestCase
from catcher import models

class Match(TournamentTestCase):

    def testGet(self):
        newTournament = self.createTournament()
        # get one id match
        matchId = self.getMatchId(newTournament['id'])
        response = self.request(
            method  = 'GET',
            path    = ('/api/match/%s' % matchId)
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(matchId, response['id'])

    def testPutActive(self):
        newTournament = self.createTournament()
        # get one id match
        matchId = self.getMatchId(newTournament['id'])
        response = self.request(
            method  = 'PUT',
            path    = ('/api/match/%s' % matchId),
            headers = self.headers,
            body    = {"active": True}
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['active'], True)
        # TODO: testovat, pokud bude zmena atributu active neco delat
        # TODO: testovat doplneni hracu do tabulek player_at_match

    def testPutTerminate(self):
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # play all matches on tournament
        self.playMatches(tournamentId)

        # check standings
        standings = models.Standing.select().where(
            models.Standing.tournamentId == tournamentId
            ).order_by(
            models.Standing.standing.asc()
            )
        self.assertEqual(len(standings), 4)
        self.assertEqual(standings[0].teamId, 3)
        self.assertEqual(standings[1].teamId, 4)
        self.assertEqual(standings[2].teamId, 2)
        self.assertEqual(standings[3].teamId, 1)

    def testPut1(self):
        newTournament = self.createTournament()
        # get one id match
        matchId = self.getMatchId(newTournament['id'])
        response = self.request(
            method  = 'PUT',
            path    = ('/api/match/%s' % matchId),
            headers = self.headers,
            body    = {"description": "Baráž"}
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['description'], u"Baráž")

    def testPut2(self):
        '''unvalid fieldId'''
        newTournament = self.createTournament()
        # get one id match
        matchId = self.getMatchId(newTournament['id'])
        response = self.request(
            method  = 'PUT',
            path    = ('/api/match/%s' % matchId),
            headers = self.headers,
            body    = {"fieldId": 2}
            )
        self.assertEqual(self.srmock.status, HTTP_400)

class MatchPoints(TournamentTestCase):
    
    def testGet(self):
        '''this test is based on init dataset!'''
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # get one id match
        matchId = self.getMatchId(tournamentId)
        self.activeMatch(matchId)
        self.playFirstFivePoints(matchId)

        response = self.request(
            method  = 'GET',
            path    = ('/api/match/%s/points' % matchId)
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(5, len(response['points']))

    def testPut(self):
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # get one id match
        matchId = self.getMatchId(tournamentId)
        self.activeMatch(matchId)
        self.playFirstFivePoints(matchId)

        response = self.request(
            method  = 'PUT',
            path    = ('/api/match/%s/point/2' % matchId),
            headers = self.headers,
            body    = {"assistPlayerId": 18, "scorePlayerId": 19}
            )
        self.assertEqual(self.srmock.status, HTTP_200)

        response = self.request(
            method  = 'PUT',
            path    = ('/api/match/%s/point/4' % matchId),
            headers = self.headers,
            body    = {"callahan": True}
            )
        self.assertEqual(self.srmock.status, HTTP_200)

        # check skore
        match =  models.Match.get(id=matchId)
        self.assertEqual(2, match.homeScore)
        self.assertEqual(3, match.awayScore)

        # check score player at tournament
        player = models.PlayerAtTournament.get(playerId=2, tournamentId=tournamentId)
        self.assertEqual(0, player.assists)
        self.assertEqual(1, player.scores)
        self.assertEqual(1, player.total)

        # check score player at tournament
        player = models.PlayerAtTournament.get(playerId=3, tournamentId=tournamentId)
        self.assertEqual(0, player.assists)
        self.assertEqual(1, player.scores)
        self.assertEqual(1, player.total)

        # check score player at tournament
        player = models.PlayerAtTournament.get(playerId=18, tournamentId=tournamentId)
        self.assertEqual(2, player.assists)
        self.assertEqual(0, player.scores)
        self.assertEqual(2, player.total)

        # check score player at match
        player = models.PlayerAtMatch.get(playerId=2, matchId=matchId)
        self.assertEqual(0, player.assists)
        self.assertEqual(1, player.scores)
        self.assertEqual(1, player.total)

        # check score player at match
        player = models.PlayerAtMatch.get(playerId=3, matchId=matchId)
        self.assertEqual(0, player.assists)
        self.assertEqual(1, player.scores)
        self.assertEqual(1, player.total)

        # check score player at match
        player = models.PlayerAtMatch.get(playerId=18, matchId=matchId)
        self.assertEqual(2, player.assists)
        self.assertEqual(0, player.scores)
        self.assertEqual(2, player.total)

        # check number of points
        pointCounter = len(models.Point.select().where(
            models.Point.matchId ==matchId
            ))
        self.assertEqual(5, pointCounter)

        # check number of callahans
        callahanCounter = len(models.Point.select().where(
            models.Point.callahan==True,
            models.Point.matchId ==matchId
            ))
        self.assertEqual(2, callahanCounter)


    def testPost1(self):
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # get one id match
        matchId = self.getMatchId(tournamentId)
        body = {
            "assistPlayerId": 3,   
            "scorePlayerId": 2,
            "homePoint": True,
            "callahan": False
            }

        # match is not active
        response = self.request(
            method  = 'POST',
            path    = ('/api/match/%s/points' % matchId),
            headers = self.headers,
            body    = body
            )
        self.assertEqual(self.srmock.status, HTTP_400)

        self.activeMatch(matchId)
        # match is active
        response = self.request(
            method  = 'POST',
            path    = ('/api/match/%s/points' % matchId),
            headers = self.headers,
            body    = body
            )
        self.assertEqual(self.srmock.status, HTTP_201)
        
        # check point
        point = models.Point.get(matchId=matchId, order=1)
        self.assertEqual(response['awayScore'], point.awayScore)
        self.assertEqual(response['matchId'], point.matchId)
        self.assertEqual(response['homePoint'], point.homePoint)
        self.assertEqual(response['scorePlayerId'], point.scorePlayerId)
        self.assertEqual(response['homeScore'], point.homeScore)
        self.assertEqual(response['callahan'], point.callahan)
        self.assertEqual(response['assistPlayerId'], point.assistPlayerId)
        self.assertEqual(response['order'], point.order)

        # check skore
        match =  models.Match.get(id=matchId)
        self.assertEqual(1, match.homeScore)
        self.assertEqual(0, match.awayScore)

        # check score player at tournament
        player = models.PlayerAtTournament.get(playerId=2, tournamentId=tournamentId)
        self.assertEqual(tournamentId, player.tournamentId)
        self.assertEqual(0, player.matches)
        self.assertEqual(2, player.playerId)
        self.assertEqual(0, player.assists)
        self.assertEqual(1, player.scores)
        self.assertEqual(1, player.total)

        # check assist player at tournament
        player = models.PlayerAtTournament.get(playerId=3, tournamentId=tournamentId)
        self.assertEqual(tournamentId, player.tournamentId)
        self.assertEqual(0, player.matches)
        self.assertEqual(3, player.playerId)
        self.assertEqual(1, player.assists)
        self.assertEqual(0, player.scores)
        self.assertEqual(1, player.total)

        # check score player at match
        player = models.PlayerAtMatch.get(playerId=2, matchId=matchId)
        self.assertEqual(matchId, player.matchId)
        self.assertEqual(2, player.playerId)
        self.assertEqual(0, player.assists)
        self.assertEqual(1, player.scores)
        self.assertEqual(1, player.total)

        # check assist player at match
        player = models.PlayerAtMatch.get(playerId=3, matchId=matchId)
        self.assertEqual(matchId, player.matchId)
        self.assertEqual(3, player.playerId)
        self.assertEqual(1, player.assists)
        self.assertEqual(0, player.scores)
        self.assertEqual(1, player.total)

    def testPost2(self):
        '''this test is based on init dataset!'''
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # get one id match
        matchId = self.getMatchId(tournamentId)
        self.activeMatch(matchId)
        self.playFirstFivePoints(matchId)
        
        # check point
        point = models.Point.get(matchId=matchId, order=5)
        self.assertEqual(3, point.awayScore)
        self.assertEqual(False, point.homePoint)
        self.assertEqual(None, point.scorePlayerId)
        self.assertEqual(2, point.homeScore)
        self.assertEqual(False, point.callahan)
        self.assertEqual(18, point.assistPlayerId)

        # check skore
        match =  models.Match.get(id=matchId)
        self.assertEqual(2, match.homeScore)
        self.assertEqual(3, match.awayScore)

        # check score player at tournament
        player = models.PlayerAtTournament.get(playerId=2, tournamentId=tournamentId)
        self.assertEqual(1, player.assists)
        self.assertEqual(1, player.scores)
        self.assertEqual(2, player.total)

        # check score player at tournament
        player = models.PlayerAtTournament.get(playerId=17, tournamentId=tournamentId)
        self.assertEqual(0, player.assists)
        self.assertEqual(2, player.scores)
        self.assertEqual(2, player.total)

        # check score player at tournament
        player = models.PlayerAtTournament.get(playerId=18, tournamentId=tournamentId)
        self.assertEqual(1, player.assists)
        self.assertEqual(0, player.scores)
        self.assertEqual(1, player.total)

        # check score player at match
        player = models.PlayerAtMatch.get(playerId=2, matchId=matchId)
        self.assertEqual(1, player.assists)
        self.assertEqual(1, player.scores)
        self.assertEqual(2, player.total)

        # check score player at match
        player = models.PlayerAtMatch.get(playerId=17, matchId=matchId)
        self.assertEqual(0, player.assists)
        self.assertEqual(2, player.scores)
        self.assertEqual(2, player.total)

        # check score player at match
        player = models.PlayerAtMatch.get(playerId=18, matchId=matchId)
        self.assertEqual(1, player.assists)
        self.assertEqual(0, player.scores)
        self.assertEqual(1, player.total)

        # check number of points
        pointCounter = len(models.Point.select().where(
            models.Point.matchId ==matchId
            ))
        self.assertEqual(5, pointCounter)

        # check number of callahans
        callahanCounter = len(models.Point.select().where(
            models.Point.callahan==True,
            models.Point.matchId ==matchId
            ))
        self.assertEqual(1, callahanCounter)

    def testDelete(self):
        '''this test is based on init dataset!'''
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # get one id match
        matchId = self.getMatchId(tournamentId)
        self.activeMatch(matchId)
        self.playFirstFivePoints(matchId)

        # delete two last points
        response = self.request(
            method  = 'DELETE',
            path    = ('/api/match/%s/points' % matchId),
            headers = self.headers
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        response = self.request(
            method  = 'DELETE',
            path    = ('/api/match/%s/points' % matchId),
            headers = self.headers
            )
        self.assertEqual(self.srmock.status, HTTP_200)

        # check number of points
        pointCounter = len(models.Point.select().where(
            models.Point.matchId ==matchId
            ))
        self.assertEqual(3, pointCounter)

        # check number of callahans
        callahanCounter = len(models.Point.select().where(
            models.Point.callahan==True,
            models.Point.matchId ==matchId
            ))
        self.assertEqual(1, callahanCounter)

        # check skore
        match =  models.Match.get(id=matchId)
        self.assertEqual(1, match.homeScore)
        self.assertEqual(2, match.awayScore)

        # check score player at tournament
        player = models.PlayerAtTournament.get(playerId=2, tournamentId=tournamentId)
        self.assertEqual(0, player.assists)
        self.assertEqual(1, player.scores)
        self.assertEqual(1, player.total)

        # check score player at tournament
        player = models.PlayerAtTournament.get(playerId=17, tournamentId=tournamentId)
        self.assertEqual(0, player.assists)
        self.assertEqual(2, player.scores)
        self.assertEqual(2, player.total)

        # check score player at tournament
        player = models.PlayerAtTournament.get(playerId=18, tournamentId=tournamentId)
        self.assertEqual(0, player.assists)
        self.assertEqual(0, player.scores)
        self.assertEqual(0, player.total)

        # check score player at match
        player = models.PlayerAtMatch.get(playerId=2, matchId=matchId)
        self.assertEqual(0, player.assists)
        self.assertEqual(1, player.scores)
        self.assertEqual(1, player.total)

        # check score player at match
        player = models.PlayerAtMatch.get(playerId=17, matchId=matchId)
        self.assertEqual(0, player.assists)
        self.assertEqual(2, player.scores)
        self.assertEqual(2, player.total)

        # check score player at match
        player = models.PlayerAtMatch.get(playerId=18, matchId=matchId)
        self.assertEqual(0, player.assists)
        self.assertEqual(0, player.scores)
        self.assertEqual(0, player.total)
