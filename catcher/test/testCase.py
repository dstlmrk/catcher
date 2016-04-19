#!/usr/bin/python
# coding=utf-8

import ujson as json
import falcon.testing
from catcher import restapi
from catcher import resources as r
from test import Database
from playhouse.shortcuts import model_to_dict
from falcon import HTTP_200, HTTP_201, HTTP_304, HTTP_400
from catcher import models
# import json

# TODO: in new Falcon version use TestCase instead TestBase
class TestCase(falcon.testing.TestBase):

    # @classmethod
    # def setUpClass(cls):
    #     Database.fill()

    # @classmethod
    # def tearDownClass(cls):
    #     Database.clean()

    def request(self, method, path, headers = None, body = None, decode = 'utf-8', queryString = None):

        if isinstance(body, dict):
            body = json.dumps(body)
        
        response = self.simulate_request(
            method       = method,
            path         = path,
            headers      = headers,
            body         = body,
            decode       = decode,
            query_string = queryString 
            )
        return json.loads(response) if response else None

    def setUp(self):
        Database.fill()

        models.Role(role="organizer").save()
        models.Role(role="admin").save()
        models.Role(role="club").save()
        models.User(
            email    = "test1@test.cz",
            password = "heslo1",
            apiKey   = "#apiKey1",
            role     = "admin"
            ).save()
        models.User(
            email    = "test2@test.cz",
            password = "heslo2",
            apiKey   = "#apiKey2",
            role     = "club",
            clubId   = 1
            ).save()
        models.User(
            email    = "test3@test.cz",
            password = "heslo3",
            apiKey   = "#apiKey3",
            role     = "organizer"
            ).save()
        # database has to be filled before call before()
        super(TestCase, self).setUp()
        # api has to be after super
        self.api = restapi.api

    def tearDown(self):
        super(TestCase, self).tearDown()
        Database.clean()

class TournamentTestCase(TestCase):

    headers = {
        "Content-Type" : "application/json",
        "Authorization": "#apiKey3"
    }

    def createTournament(self):
        '''this method is used by tests for creating test tournament'''
        body = {
            "name": "PFL 2016",
            "city": "Prague",
            "country": "CZE",
            "startDate": "2016-04-01",
            "endDate": "2016-04-01",
            "divisionId": 1,
            "caldTournamentId": None,
            "teams": [{
                "id": 1,
                "seeding": 1
            }, {
                "id": 2,
                "seeding": 2
            }, {
                "id": 3,
                "seeding": 3
            }, {
                "id": 4,
                "seeding": 4
            }],
            "fieldsCount": 1,
            "fields": [{
                "id": 1,
                "name": "Main field"
            }],
            "groups": [

            ],
            "matches": [{
                "fieldId": 1,
                "startTime": "2016-04-01T09:00:00",
                "endTime": "2016-04-01T09:29:00",
                "homeSeed": 1,
                "awaySeed": 4,
                "looserNextStep": "3RD",
                "winnerNextStep": "FIN",
                "looserFinalStanding": None,
                "winnerFinalStanding": None,
                "identificator": "SE1",
                "description": None
            }, {
                "fieldId": 1,
                "startTime": "2016-04-01T09:30:00",
                "endTime": "2016-04-01T09:59:00",
                "homeSeed": 2,
                "awaySeed": 3,
                "looserNextStep": "3RD",
                "winnerNextStep": "FIN",
                "looserFinalStanding": None,
                "winnerFinalStanding": None,
                "identificator": "SE2",
                "description": None
            }, {
                "fieldId": 1,
                "startTime": "2016-04-01T10:00:00",
                "endTime": "2016-04-01T10:29:00",
                "homeSeed": None,
                "awaySeed": None,
                "looserNextStep": None,
                "winnerNextStep": None,
                "looserFinalStanding": 4,
                "winnerFinalStanding": 3,
                "identificator": "3RD",
                "description": None
            }, {
                "fieldId": 1,
                "startTime": "2016-04-01T10:30:00",
                "endTime": "2016-04-01T10:59:00",
                "homeSeed": None,
                "awaySeed": None,
                "looserNextStep": None,
                "winnerNextStep": None,
                "looserFinalStanding": 2,
                "winnerFinalStanding": 1,
                "identificator": "FIN",
                "description": "Finale"
            }]
        }
        response = self.request(
            method  = 'POST',
            path    = '/api/tournaments',
            headers = self.headers,
            body    = body
            )
        self.assertEqual(self.srmock.status, HTTP_201)
        return response

    def createRosters(self, tournamentId):
        '''this method is used by tests for creating rosters (5 player for 4 teams)'''
        playerId = 1
        for teamId in range(1,5):
            for i in range(0,5):
                self.request(
                    method  = 'POST',
                    path    = ('/api/tournament/%s/players' % (tournamentId)),
                    headers = self.headers,
                    body    = {"playerId": playerId,"teamId": teamId}
                    )
                self.assertEqual(self.srmock.status, HTTP_201)
                playerId += 1

    def getMatchId(self, tournamentId):
        match = models.Match.select().where(
            models.Match.tournamentId == tournamentId
            )[0]
        return match.id

    def readyTournament(self, tournamentId):
        response = self.request(
            method  = 'PUT',
            path    = ('/api/tournament/%s' % tournamentId),
            headers = self.headers,
            body    = {"ready": True}
            )
        self.assertEqual(self.srmock.status, HTTP_200)

    def terminateTournament(self, tournamentId):
        response = self.request(
            method  = 'PUT',
            path    = ('/api/tournament/%s' % tournamentId),
            headers = self.headers,
            body    = {"terminated": True}
            )
        self.assertEqual(self.srmock.status, HTTP_200)

    def activeMatch(self, matchId):
        response = self.request(
            method  = 'PUT',
            path    = ('/api/match/%s' % matchId),
            headers = self.headers,
            body    = {"active": True}
            )
        self.assertEqual(self.srmock.status, HTTP_200)

    def playFirstFivePoints(self, matchId,
        homePlayers = [1,2,3,4,5], awayPlayers = [16, 17, 18, 19, 20]):
        response = self.request(
            method  = 'POST',
            path    = ('/api/match/%s/points' % matchId),
            headers = self.headers,
            body    = {
                "assistPlayerId": homePlayers[0],   
                "scorePlayerId": homePlayers[1],
                "homePoint": True
                }
            )
        self.assertEqual(self.srmock.status, HTTP_201)
        response = self.request(
            method  = 'POST',
            path    = ('/api/match/%s/points' % matchId),
            headers = self.headers,
            body    = {
                "assistPlayerId": awayPlayers[0],   
                "scorePlayerId": awayPlayers[1],
                "homePoint": False
                }
            )
        self.assertEqual(self.srmock.status, HTTP_201)
        response = self.request(
            method  = 'POST',
            path    = ('/api/match/%s/points' % matchId),
            headers = self.headers,
            body    = {  
                "scorePlayerId": awayPlayers[1],
                "homePoint": False,
                "callahan": True
                }
            )
        self.assertEqual(self.srmock.status, HTTP_201)
        response = self.request(
            method  = 'POST',
            path    = ('/api/match/%s/points' % matchId),
            headers = self.headers,
            body    = {
                "assistPlayerId": homePlayers[1],   
                "scorePlayerId": homePlayers[2],
                "homePoint": True
                }
            )
        self.assertEqual(self.srmock.status, HTTP_201)
        response = self.request(
            method  = 'POST',
            path    = ('/api/match/%s/points' % matchId),
            headers = self.headers,
            body    = {
                "assistPlayerId": awayPlayers[2],
                "scorePlayerId": None,
                "homePoint": False
                }
            )
        self.assertEqual(self.srmock.status, HTTP_201)

    def playMatches(self, tournamentId):
        # prvni udelam dva zapasy, pak dalsi dva
        matches = models.Match.select().where(
            models.Match.tournamentId == tournamentId
            ).order_by(
            models.Match.startTime.asc()
            ).limit(2)

        for match in matches:
            players = models.PlayerAtTournament.select().where(
                models.PlayerAtTournament.tournamentId == tournamentId,
                models.PlayerAtTournament.teamId == match.homeTeamId
                )
            homePlayers = []
            for player in players:
                homePlayers.append(player.playerId)
            players = models.PlayerAtTournament.select().where(
                models.PlayerAtTournament.tournamentId == tournamentId,
                models.PlayerAtTournament.teamId == match.awayTeamId
                )
            awayPlayers = []
            for player in players:
                awayPlayers.append(player.playerId)

            # active match
            self.activeMatch(match.id)
            # play some points
            self.playFirstFivePoints(match.id, homePlayers, awayPlayers)
            # terminate match
            response = self.request(
                method  = 'PUT',
                path    = ('/api/match/%s' % match.id),
                headers = self.headers,
                body    = {"terminated": True}
                )
            self.assertEqual(self.srmock.status, HTTP_200)

        # dalsi dva zapasy, kde uz jsou dosazene tymy
        matches = models.Match.select().where(
            models.Match.tournamentId == tournamentId
            ).order_by(
            models.Match.startTime.asc()
            ).limit(2).offset(2)

        for match in matches:
            players = models.PlayerAtTournament.select().where(
                models.PlayerAtTournament.tournamentId == tournamentId,
                models.PlayerAtTournament.teamId == match.homeTeamId
                )
            homePlayers = []
            for player in players:
                homePlayers.append(player.playerId)
            players = models.PlayerAtTournament.select().where(
                models.PlayerAtTournament.tournamentId == tournamentId,
                models.PlayerAtTournament.teamId == match.awayTeamId
                )
            awayPlayers = []
            for player in players:
                awayPlayers.append(player.playerId)

            # active match
            self.activeMatch(match.id)
            # play some points
            self.playFirstFivePoints(match.id, homePlayers, awayPlayers)
            # terminate match

            response = self.request(
                method  = 'PUT',
                path    = ('/api/match/%s' % match.id),
                headers = self.headers,
                body    = {"terminated": True}
                )
            self.assertEqual(self.srmock.status, HTTP_200)

    def surrenderSpirit(self, tournamentId):
        matches = models.Match.select().where(
            models.Match.tournamentId == tournamentId
            ).order_by(models.Match.startTime.desc())

        self.assertEqual(4, len(matches))
        
        match = None
        for match in matches:

            response = self.request(
                method  = 'POST',
                path    = ('/api/match/%s/spirits' % match.id),
                headers = self.headers,
                body    = {
                    "teamId": match.homeTeamId,
                    "comment": "Game was very agresive, but fair",
                    "rules": 3,
                    "fouls": 1,
                    "fair": 4,
                    "positive": 2,
                    "communication": 2
                    }
                )
            self.assertEqual(self.srmock.status, HTTP_201)
            # check response vs database
            spirit = models.Spirit.get(matchId=match.id, teamId=match.homeTeamId)
            self.assertEqual(response['matchId'], spirit.matchId)
            self.assertEqual(response['teamId'], spirit.teamId)
            self.assertEqual(response['comment'], spirit.comment)
            self.assertEqual(response['rules'], spirit.rules)
            self.assertEqual(response['fouls'], spirit.fouls)
            self.assertEqual(response['fair'], spirit.fair)
            self.assertEqual(response['positive'], spirit.positive)
            self.assertEqual(response['communication'], spirit.communication)
            self.assertEqual(response['givingTeamId'], spirit.givingTeamId)
            self.assertEqual(response['total'], 12)

            response = self.request(
                method  = 'POST',
                path    = ('/api/match/%s/spirits' % match.id),
                headers = self.headers,
                body    = {
                    "teamId": match.awayTeamId,
                    "comment": "Game was very agresive, but fair",
                    "rules": 2,
                    "fouls": 2,
                    "fair": 2,
                    "positive": 2,
                    "communication": 2
                    }
                )
            self.assertEqual(self.srmock.status, HTTP_201)
            # check response vs database
            spirit = models.Spirit.get(matchId=match.id, teamId=match.awayTeamId)
            self.assertEqual(response['matchId'], spirit.matchId)
            self.assertEqual(response['teamId'], spirit.teamId)
            self.assertEqual(response['comment'], spirit.comment)
            self.assertEqual(response['rules'], spirit.rules)
            self.assertEqual(response['fouls'], spirit.fouls)
            self.assertEqual(response['fair'], spirit.fair)
            self.assertEqual(response['positive'], spirit.positive)
            self.assertEqual(response['communication'], spirit.communication)
            self.assertEqual(response['givingTeamId'], spirit.givingTeamId)
            self.assertEqual(response['total'], 10)

            _match = models.Match.get(id=match.id)
            self.assertEqual(_match.spiritHome, 12)
            self.assertEqual(_match.spiritAway, 10)

        return match