#!/usr/bin/python
# coding=utf-8

from testCase import TestCase
from falcon import HTTP_200, HTTP_201, HTTP_400
from catcher import models

class Players(TestCase):

    def testPost1(self):
        '''new player'''
        body = {
          "firstname": "Karel",
          "lastname": "Novák",
          "nickname": "Kája",
          "number": 9,
          "caldId": None,
          "clubId": 1
        }
        
        headers = {"Content-Type": "application/json"}
        response = self.request(
            method  = 'POST',
            path    = '/api/players',
            headers = headers,
            body    = body
            )

        expectedResponse = {
          "firstname": "Karel",
          "lastname": u"Novák",
          "nickname": u"Kája",
          "number": 9,
          "ranking": None,
          "caldId": None,
          "clubId": 1
        }

        # I can't know, what id is there
        del response['id']
        self.assertEqual(response, expectedResponse)
        self.assertEqual(self.srmock.status, HTTP_201)

    def testPost2(self):
        '''new player with unvalid type of number'''
        body = {
          "firstname": "Karel",
          "lastname": "Novák",
          "nickname": "Kája",
          "number": "nine",
          "caldId": None,
          "clubId": 1
        }
        headers = {"Content-Type": "application/json"}
        response = self.request(
            method  = 'POST',
            path    = '/api/players',
            headers = headers,
            body    = body
            )
        self.assertEqual(self.srmock.status, HTTP_400)

    def testGet(self):
        players = len(models.Player.select())        
        response = self.request(
            method  = 'GET',
            path    = '/api/players',
            decode  = 'utf-8'
            )
        self.assertEqual(response['count'], players)
        self.assertEqual(self.srmock.status, HTTP_200)

class Player(TestCase):

    def testGet(self):
        player = models.Player.select().where(models.Player.id == 1).get()        
        response = self.request(
            method  = 'GET',
            path    = '/api/player/1',
            decode  = 'utf-8'
            )
        self.assertEqual(response['id'], player.id)
        self.assertEqual(response['caldId'], player.caldId)
        self.assertEqual(response['firstname'], player.firstname)
        self.assertEqual(response['lastname'], player.lastname)
        self.assertEqual(response['nickname'], player.nickname)
        self.assertEqual(response['number'], player.number)
        self.assertEqual(response['clubId'], player.clubId)
        self.assertEqual(self.srmock.status, HTTP_200)

    def testPut(self):
        '''change some columns'''
        body = {
          "firstname": "Kateřina",
          "lastname": "Malá",
          "nickname": "Katy",
          "number": 99
        }
        
        headers = {"Content-Type": "application/json"}
        
        response = self.request(
            method  = 'PUT',
            path    = '/api/player/1',
            headers = headers,
            body    = body
            )

        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['firstname'], u"Kateřina")
        self.assertEqual(response['lastname'], u"Malá")
        self.assertEqual(response['nickname'], "Katy")
        self.assertEqual(response['number'], 99)

    def testDelete(self):
        player = models.Player.select().where(models.Player.id == 2).get()
        response = self.request(
            method  = 'DELETE',
            path    = '/api/player/2'
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        with self.assertRaises(models.Player.DoesNotExist):
            player = models.Player.select().where(models.Player.id == 2).get()