#!/usr/bin/python
# coding=utf-8

from testCase import TournamentTestCase
from falcon import HTTP_200, HTTP_201, HTTP_400, HTTP_401
from catcher import models

class Group(TournamentTestCase):

    def testPost1(self):
        '''create tournament with groups'''
        tournament = self.createLeague()
        self.readyTournament(tournament['id'])
        self.createRosters(tournament['id'], tournament['teams'])

        matches = models.Match.select().where(models.Match.tournamentId==tournament['id'])
        
        for match in matches:
            print "ZAPAS", match
            response = self.request(
                    method  = 'PUT',
                    path    = ('/api/match/%s' % match.id),
                    headers = self.headers,
                    body    = {
                        "active"    : True,
                        "terminated": True,
                        "homeScore" : 1,
                        "awayScore" : 2
                        }
                    )
            print response
            self.assertEqual(self.srmock.status, HTTP_200)

        response = self.request(
            method  = 'GET',
            path    = ('/api/tournament/%s/standings' % tournament['id']),
            headers = {"Content-Type": "application/json"}
            )

        print response
        self.assertEqual(self.srmock.status, HTTP_200)
        standings = response['standings']
        self.assertEqual(standings[0]['teamId'], 3)
        self.assertEqual(standings[1]['teamId'], 2)
        self.assertEqual(standings[2]['teamId'], 1)

    def testPost2(self):
        '''create tournament with groups and playoffs'''
        body = {
            "name": "Champions League 2016",
            "city": "Prague",
            "country": "CZE",
            "startDate": "2016-08-01",
            "endDate": "2016-08-01",
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
            "groups": [{
                "ide": "A",
                "teams": [{
                    "id": 1
                }, {
                    "id": 2
                }],
                "advancements": [{
                    "standing": 1,
                    "nextStepIde": "FIN",
                    "finalStanding": None
                }, {
                    "standing": 2,
                    "nextStepIde": "3RD",
                    "finalStanding": None
                }],
                "matches": [{
                    "fieldId": 1,
                    "startTime": "2016-08-01T09:00:00",
                    "endTime": "2016-08-01T09:29:00",
                    "homeSeed": 1,
                    "awaySeed": 2,
                    "winner": {
                        "nextStepIde": None,
                        "finalStanding": None
                    },
                    "looser": {
                        "nextStepIde": None,
                        "finalStanding": None
                    },
                    "ide": "A1",
                    "description": None
                }]
            }, {
                "ide": "B",
                "teams": [{
                    "id": 3
                }, {
                    "id": 4
                }],
                "advancements": [{
                    "standing": 1,
                    "nextStepIde": "FIN",
                    "finalStanding": None
                }, {
                    "standing": 2,
                    "nextStepIde": "3RD",
                    "finalStanding": None
                }],
                "matches": [{
                    "fieldId": 1,
                    "startTime": "2016-08-01T09:30:00",
                    "endTime": "2016-08-01T09:59:00",
                    "homeSeed": 3,
                    "awaySeed": 4,
                    "winner": {
                        "nextStepIde": None,
                        "finalStanding": None
                    },
                    "looser": {
                        "nextStepIde": None,
                        "finalStanding": None
                    },
                    "ide": "B1",
                    "description": None
                }]
            }],

            "playoff": [{
                "fieldId": 1,
                "startTime": "2016-08-01T10:00:00",
                "endTime": "2016-08-01T10:29:00",
                "homeSeed": None,
                "awaySeed": None,
                "winner": {
                    "nextStepIde": None,
                    "finalStanding": 3
                },
                "looser": {
                    "nextStepIde": None,
                    "finalStanding": 4
                },
                "ide": "3RD",
                "description": None
            }, {
                "fieldId": 1,
                "startTime": "2016-08-01T10:30:00",
                "endTime": "2016-08-01T10:59:00",
                "homeSeed": None,
                "awaySeed": None,
                "winner": {
                    "nextStepIde": None,
                    "finalStanding": 1
                },
                "looser": {
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
            headers = self.headers,
            body    = body
            )
        self.assertEqual(self.srmock.status, HTTP_201)
        tournamentId = response['id']

        self.readyTournament(tournamentId)

        matches = models.Match.select().where(
            models.Match.tournamentId == tournamentId
            )
        
        for match in matches:
            print "ZAPAS", match
            response = self.request(
                    method  = 'PUT',
                    path    = ('/api/match/%s' % match.id),
                    headers = self.headers,
                    body    = {
                        "active"    : True,
                        "terminated": True,
                        "homeScore" : 1,
                        "awayScore" : 2
                        }
                    )
            print response
            self.assertEqual(self.srmock.status, HTTP_200)


        response = self.request(
            method  = 'GET',
            path    = ('/api/tournament/%s/standings' % tournamentId),
            headers = {"Content-Type": "application/json"}
            )

        print response
        self.assertEqual(self.srmock.status, HTTP_200)
        standings = response['standings']
        self.assertEqual(standings[0]['teamId'], 4)
        self.assertEqual(standings[1]['teamId'], 2)
        self.assertEqual(standings[2]['teamId'], 3)
        self.assertEqual(standings[3]['teamId'], 1)

    def testGet(self):
        '''create tournament with groups'''
        tournament = self.createLeague()

        response = self.request(
            method  = 'GET',
            path    = ('/api/tournament/%s' % tournament['id']),
            headers = self.headers
            )
        
        print response