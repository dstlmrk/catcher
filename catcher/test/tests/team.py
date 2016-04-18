#!/usr/bin/python
# coding=utf-8

from testCase import TestCase
from falcon import HTTP_200, HTTP_201, HTTP_400
from catcher import models

class Teams(TestCase):

    def testGet(self):
        teams = len(models.Team.select())        
        response = self.request(
            method  = 'GET',
            path    = '/api/teams',
            decode  = 'utf-8'
            )
        self.assertEqual(response['count'], teams)
        self.assertEqual(self.srmock.status, HTTP_200)

    def testPost1(self):
        body = {
            "clubId": 12,
            "degree": "A",
            "divisionId": 2
            }
        headers = {
            "Content-Type" : "application/json",
            "Authorization": "#apiKey1"
            }
        response = self.request(
            method  = 'POST',
            path    = '/api/teams',
            headers = headers,
            body    = body
            )

        expectedResponse = {
            "clubId": 12,
            "degree": "A",
            "divisionId": 2
            }

        # I can't know, what id is there
        del response['id']
        self.assertEqual(response, expectedResponse)
        self.assertEqual(self.srmock.status, HTTP_201)

    def testPost2(self):
        '''create team with unvalid club id'''
        body = {
            "clubId": 999999,
            "degree": "A",
            "divisionId": 2
            }
        headers = {
            "Content-Type" : "application/json",
            "Authorization": "#apiKey1"
            }
        response = self.request(
            method  = 'POST',
            path    = '/api/teams',
            headers = headers,
            body    = body
            )
        expectedResponse = {
            "clubId": 12,
            "degree": "A",
            "divisionId": 2
            }
        self.assertEqual(self.srmock.status, HTTP_400)

class Team(TestCase):

    def testGet(self):
        team = models.Team.select().where(models.Team.id == 1).get()        
        club = models.Club.select().where(models.Club.id == team.clubId).get()
        name = club.name + " " + team.degree
        response = self.request(
            method  = 'GET',
            path    = '/api/team/1',
            decode  = 'utf-8'
            )
        self.assertEqual(response['id'], team.id)
        self.assertEqual(response['clubId'], team.clubId)
        self.assertEqual(response['degree'], team.degree)
        self.assertEqual(response['divisionId'], team.divisionId)
        self.assertEqual(response['name'], name)
        self.assertEqual(self.srmock.status, HTTP_200)

    def testPut(self):
        '''change shortcut, city and country'''
        body = {
          "degree": 'B',
          "divisionId": 4
        }
        
        headers = {
            "Content-Type" : "application/json",
            "Authorization": "#apiKey1"
            }
        
        response = self.request(
            method  = 'PUT',
            path    = '/api/team/16',
            headers = headers,
            body    = body
            )

        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['degree'], 'B')
        self.assertEqual(response['divisionId'], 4)

    def testDelete(self):
        club = models.Team.select().where(models.Team.id == 15).get()
        response = self.request(
            method  = 'DELETE',
            path    = '/api/team/15',
            headers = {
                "Authorization": "#apiKey1"
                }
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        with self.assertRaises(models.Team.DoesNotExist):
            club = models.Team.select().where(models.Team.id == 15).get()