#!/usr/bin/python
# coding=utf-8

from testCase import TournamentTestCase
from falcon import HTTP_200, HTTP_201, HTTP_304, HTTP_400
from catcher import models
from datetime import datetime

class Tournaments(TournamentTestCase):

    def testPost0(self):
        self.createLeague()

    def testPost1(self):
        '''new tournament'''
        response = self.createTournament()
        expectedResponse = {
            "name": "PFL 2016",
            "city": "Prague",
            "country": "CZE",
            "startDate": "2016-04-01T00:00:00",
            "endDate": "2016-04-01T00:00:00",
            "divisionId": 1,
            "caldTournamentId": None,
            "teams": 4,
            "ready": False,
            "terminated": False
            }
        # I can't know, what id is there
        del response['id']
        del response['userId']

        self.assertEqual(response, expectedResponse)
        self.assertEqual(self.srmock.status, HTTP_201)

    def testPost2(self):
        '''create tournament with unvalid values'''
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
            "playoff": [{
                "fieldId": 1,
                "startTime": "2016-04-01T09:00:00",
                "endTime": "2016-04-01T09:29:00",
                "homeSeed": 1,
                "awaySeed": 4,
                "winner":{
                    "nextStepIde": "FIN",
                    "finalStanding": None
                },
                "looser":{
                    "nextStepIde": "3RD",
                    "finalStanding": None
                },
                "ide": "SE1",
                "description": None
            }, {
                "fieldId": 1,
                "startTime": "2016-04-01T09:30:00",
                "endTime": "2016-04-01T09:59:00",
                "homeSeed": 2,
                "awaySeed": 3,
                "winner":{
                    "nextStepIde": "FIN",
                    "finalStanding": None
                },
                "looser":{
                    "nextStepIde": "3RD",
                    "finalStanding": None
                },
                "ide": "SE2",
                "description": None
            }, {
                "fieldId": 1,
                "startTime": "2016-04-01T10:00:00",
                "endTime": "2016-04-01T10:29:00",
                "homeSeed": None,
                "awaySeed": None,
                "winner":{
                    "nextStepIde": None,
                    "finalStanding": 3
                },
                "looser":{
                    "nextStepIde": None,
                    "finalStanding": 4
                },
                "ide": "3RD",
                "description": None
            }, {
                "fieldId": 1,
                "startTime": "2016-04-01T09:30:00",
                "endTime": "2016-04-01T10:59:00",
                "homeSeed": None,
                "awaySeed": None,
                "winner":{
                    "nextStepIde": None,
                    "finalStanding": 1
                },
                "looser":{
                    "nextStepIde": None,
                    "finalStanding": 2
                },
                "ide": "FIN",
                "description": "Finale"
            }]
        }

        response = self.request(
            method  = 'POST',
            path    = '/api/tournaments',
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "#apiKey3"
            },
            body    = body
            )

        # self.assertEqual(response['description'], "In match FI won't play two teams")
        self.assertEqual(self.srmock.status, HTTP_400)

    def testGet(self):
        tournaments = len(models.Tournament.select())        
        response = self.request(
            method  = 'GET',
            path    = '/api/tournaments'
            )
        self.assertEqual(response['count'], tournaments)
        self.assertEqual(self.srmock.status, HTTP_200)

class Tournament(TournamentTestCase):

    def testGet(self):
        newTournament = self.createTournament()
        tournament = models.Tournament.select().where(
            models.Tournament.id == newTournament['id']
            ).get()

        response = self.request(
            method  = 'GET',
            path    = ('/api/tournament/%s' % newTournament['id'])
            )

        self.assertEqual(response['id'], tournament.id)
        self.assertEqual(response['city'], tournament.city)
        self.assertEqual(
            datetime.strptime(response['endDate'], "%Y-%m-%dT%H:%M:%S"),
            tournament.endDate
            )
        self.assertEqual(response['name'], tournament.name)
        self.assertEqual(response['divisionId'], tournament.divisionId)
        self.assertEqual(response['country'], tournament.country)
        self.assertEqual(response['teams'], tournament.teams)
        self.assertEqual(response['caldTournamentId'], tournament.caldTournamentId)
        self.assertEqual(response['ready'], tournament.ready)
        self.assertEqual(response['terminated'], tournament.terminated)
        self.assertEqual(
            datetime.strptime(response['startDate'], "%Y-%m-%dT%H:%M:%S"),
            tournament.startDate
            )
        self.assertEqual(self.srmock.status, HTTP_200)

    def testPut(self):
        '''change some columns'''
        newTournament = self.createTournament()

        body = '''{
          "name": "Champions League",
          "startDate": "2018-10-28",
          "endDate": "2018-10-29",
          "city": "Berlin",
          "country": "DEU",
          "caldTournamentId": null
        }'''
        
        response = self.request(
            method  = 'PUT',
            path    = ('/api/tournament/%s' % newTournament['id']),
            headers = self.headers,
            body    = body
            )

        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['name'], "Champions League")
        self.assertEqual(response['startDate'], "2018-10-28T00:00:00")
        self.assertEqual(response['endDate'], "2018-10-29T00:00:00")
        self.assertEqual(response['city'], "Berlin")
        self.assertEqual(response['country'], "DEU")
        self.assertEqual(response['caldTournamentId'], None)

    def testPut2(self):
        '''request with unvalid columns'''
        newTournament = self.createTournament()
        body = {"read": True}
        response = self.request(
            method  = 'PUT',
            path    = ('/api/tournament/%s' % newTournament['id']),
            headers = self.headers,
            body    = body
            )
        self.assertEqual(self.srmock.status, HTTP_304)

    def testPutReady(self):
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        response = self.request(
            method  = 'PUT',
            path    = ('/api/tournament/%s' % tournamentId),
            headers = self.headers,
            body    = {"ready": True}
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        standings = len(models.Standing.select().where(
            models.Standing.tournamentId == tournamentId)
            )
        self.assertEqual(standings, newTournament['teams'])
        # TODO: check, if teams are in matches

        team = models.TeamAtTournament.select().where(
                models.TeamAtTournament.tournamentId == tournamentId
            )[0]
        spiritAvg = models.SpiritAvg.get(tournamentId=tournamentId, teamId=team.teamId)
        self.assertEqual(0, spiritAvg.matches)
        self.assertEqual(0, spiritAvg.communication)
        self.assertEqual(0, spiritAvg.communicationGiven)
        self.assertEqual(0, spiritAvg.fair)
        self.assertEqual(0, spiritAvg.fairGiven)
        self.assertEqual(0, spiritAvg.fouls)
        self.assertEqual(0, spiritAvg.foulsGiven)
        self.assertEqual(0, spiritAvg.positive)
        self.assertEqual(0, spiritAvg.positiveGiven)
        self.assertEqual(0, spiritAvg.rules)
        self.assertEqual(0, spiritAvg.rulesGiven)
        self.assertEqual(0, spiritAvg.total)
        self.assertEqual(0, spiritAvg.totalGiven)
    
    def testTerminate1(self):
        newTournament = self.createTournament()
        response = self.request(
            method  = 'PUT',
            path    = ('/api/tournament/%s' % newTournament['id']),
            headers = self.headers,
            body    = {"terminated": True}
            )
        self.assertEqual(self.srmock.status, HTTP_400)

    def testTerminate2(self):
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)

        # play all matches on tournament
        self.playMatches(tournamentId)
        self.surrenderSpirit(tournamentId)
        # terminate tournament
        response = self.request(
            method  = 'PUT',
            path    = ('/api/tournament/%s' % newTournament['id']),
            headers = self.headers,
            body    = {"terminated": True}
            )
        self.assertEqual(self.srmock.status, HTTP_200)

class TournamentPlayers(TournamentTestCase):
    
    def testGet1(self):
        newTournament = self.createTournament()
        self.readyTournament(newTournament['id'])
        self.createRosters(newTournament['id'])
        players = len(models.PlayerAtTournament.select().where(
            models.PlayerAtTournament.tournamentId ==  newTournament['id']
            ))
        response = self.request(
            method  = 'GET',
            path    = ('/api/tournament/%s/players' % newTournament['id'])
            )
        self.assertEqual(response['count'], players)
        self.assertEqual(self.srmock.status, HTTP_200)

    def testGet2(self):
        teamId = 1
        newTournament = self.createTournament()
        self.readyTournament(newTournament['id'])
        self.createRosters(newTournament['id'])
        players = len(models.PlayerAtTournament.select().where(
            models.PlayerAtTournament.tournamentId ==  newTournament['id'],
            models.PlayerAtTournament.teamId == teamId
            ))

        response = self.request(
            method      = 'GET',
            path        = ('/api/tournament/%s/players' % (newTournament['id'])),
            queryString = 'teamId=1'
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['count'], players)

    def testPost(self):
        newTournament = self.createTournament()
        self.readyTournament(newTournament['id'])
        response = self.request(
            method  = 'POST',
            path    = ('/api/tournament/%s/players' % (newTournament['id'])),
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "#apiKey3"
                },
            body    = {"playerId": 1,"teamId": 1}
            )

        self.assertEqual(self.srmock.status, HTTP_201)
        self.assertEqual(response['matches'], 0)
        self.assertEqual(response['playerId'], 1)
        self.assertEqual(response['teamId'], 1)
        self.assertEqual(response['assists'], 0)
        self.assertEqual(response['tournamentId'], newTournament['id'])
        self.assertEqual(response['scores'], 0)
        self.assertEqual(response['total'], 0)
    
    def testDelete(self):
        '''create player and delete him'''
        newTournament = self.createTournament()
        self.readyTournament(newTournament['id'])
        response = self.request(
            method  = 'POST',
            path    = ('/api/tournament/%s/players' % (newTournament['id'])),
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "#apiKey2"
                },
            body    = {"playerId": 1,"teamId": 1}
            )
        self.assertEqual(self.srmock.status, HTTP_201)

        response = self.request(
            method  = 'DELETE',
            path    = ('/api/tournament/%s/players' % (newTournament['id'])),
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "#apiKey2"
                },
            body    = {"playerId":1,"teamId":1}
            )

        with self.assertRaises(models.PlayerAtTournament.DoesNotExist):
            models.PlayerAtTournament.get(
                playerId = 1,
                tournamentId = 1
            )

class TournamentTeams(TournamentTestCase):
    
    def testGet(self):
        newTournament = self.createTournament()

        teams = len(models.TeamAtTournament.select().where(
            models.TeamAtTournament.tournamentId == newTournament['id']
            ))
        response = self.request(
            method      = 'GET',
            path        = ('/api/tournament/%s/teams' % (newTournament['id']))
            )

        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['count'], teams)

    def testPut(self):
        newTournament = self.createTournament()

        response = self.request(
            method  = 'PUT',
            path    = ('/api/tournament/%s/teams' % newTournament['id']),
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "#apiKey3"
                },
            body    = {"seeding": 2, "teamId": 5}
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['teamId'], 5)
        self.assertEqual(response['tournamentId'], newTournament['id'])
        self.assertEqual(response['seeding'], 2)

        team = models.TeamAtTournament.get(
            tournamentId = newTournament['id'],
            seeding = 2
            )
        self.assertEqual(team.teamId, 5)

        # if tournament has ready on true, teams can't be changed
        response = self.request(
            method  = 'PUT',
            path    = ('/api/tournament/%s' % newTournament['id']),
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "#apiKey3"
                },
            body    = {"ready": True}
            )
        self.assertEqual(self.srmock.status, HTTP_200)

        response = self.request(
            method  = 'PUT',
            path    = ('/api/tournament/%s/teams' % newTournament['id']),
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "#apiKey3"
                },
            body    = {"seeding": 2, "teamId": 6}
            )
        self.assertEqual(self.srmock.status, HTTP_400)

class TournamentMatches(TournamentTestCase):
    
    def testGet(self):
        newTournament = self.createTournament()
        matches = len(models.Match.select().where(
            models.Match.tournamentId == newTournament['id']
            ))
        response = self.request(
            method      = 'GET',
            path        = ('/api/tournament/%s/matches' % (newTournament['id']))
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['count'], matches)

    def testGet2(self):
        newTournament = self.createTournament()
        matches = len(models.Match.select().where(
            models.Match.tournamentId == newTournament['id'],
            models.Match.fieldId == 1
            ))
        response = self.request(
            method      = 'GET',
            path        = ('/api/tournament/%s/matches' % (newTournament['id'])),
            queryString = 'fieldId=1'
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['count'], matches)
        