#!/usr/bin/python
# coding=utf-8

from testCase import TestCase
from falcon import HTTP_200, HTTP_201, HTTP_400
from catcher import models

class Tournaments(TestCase):

    def testPost1(self):
        '''new tournament'''
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
                "field": 1,
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
                "field": 1,
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
                "field": 1,
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
                "field": 1,
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
        
        headers = {"Content-Type": "application/json"}
        response = self.request(
            method  = 'POST',
            path    = '/api/tournaments',
            headers = headers,
            body    = body
            )

        expectedResponse = {
            "name": "PFL 2016",
            "city": "Prague",
            "country": "CZE",
            "startDate": "2016-04-01T00:00:00",
            "endDate": "2016-04-01T00:00:00",
            "divisionId": 1,
            "caldTournamentId": None,
            "teams": 4,
            "active": False,
            "ready": False,
            "terminated": False
            }

        # I can't know, what id is there
        del response['id']
        self.assertEqual(response, expectedResponse)
        self.assertEqual(self.srmock.status, HTTP_201)

    def testPost2(self):
        pass

    def testGet(self):
        pass

class Tournament(TestCase):

    def testGet(self):
        pass

    def testPut(self):
        pass