#!/usr/bin/python
# coding=utf-8

from testCase import TestCase
from falcon import HTTP_200, HTTP_201, HTTP_400, HTTP_401
from catcher import models

class Clubs(TestCase):

    def testPost1(self):
        '''new club'''
        body = {
          "caldId": None,
          "name": "Black Eagles",
          "city": "Brno",
          "country": "CZE",
          "shortcut": "BEG",
          "user": None
        }
        headers = {
            "Content-Type" : "application/json",
            "Authorization": "#apiKey1"
            }
        response = self.request(
            method  = 'POST',
            path    = '/api/clubs',
            headers = headers,
            body    = body
            )

        expectedResponse = {
          "caldId": None,
          "name": "Black Eagles",
          "city": "Brno",
          "country": "CZE",
          "shortcut": "BEG",
          "user": None
        }

        # I can't know, what id is there
        del response['id']
        self.assertEqual(response, expectedResponse)
        self.assertEqual(self.srmock.status, HTTP_201)

    def testPost2(self):
        '''new club with unvalid country columnn'''
        body = '''{
          "caldId": null,
          "name": "Black Eagles",
          "city": "Brno",
          "country": "WWW",
          "shortcut": "BEG",
          "user": null
        }
        '''
        headers = {
            "Content-Type" : "application/json",
            "Authorization": "#apiKey1"
            }
        response = self.request(
            method  = 'POST',
            path    = '/api/clubs',
            headers = headers,
            body    = body
            )
        self.assertEqual(response['description'], "'Country by ISO 3166-1 alpha-3 not found'")
        self.assertEqual(self.srmock.status, HTTP_400)

    def testGet(self):
        clubs = len(models.Club.select())        
        response = self.request(
            method  = 'GET',
            path    = '/api/clubs',
            decode  = 'utf-8'
            )
        self.assertEqual(response['count'], clubs)
        self.assertEqual(self.srmock.status, HTTP_200)

class Club(TestCase):

    def testGet(self):
        club = models.Club.select().where(models.Club.id == 1).get()        
        response = self.request(
            method  = 'GET',
            path    = '/api/club/1',
            decode  = 'utf-8'
            )
        self.assertEqual(response['id'], club.id)
        self.assertEqual(response['caldId'], club.caldId)
        self.assertEqual(response['name'], club.name)
        self.assertEqual(response['city'], club.city)
        self.assertEqual(response['country'], club.country)
        self.assertEqual(response['shortcut'], club.shortcut)
        self.assertEqual(self.srmock.status, HTTP_200)

    def testPut1(self):
        '''change shortcut, city and country by admin'''
        body = {
          "city": "Mohelnice",
          "country": "CZE",
          "shortcut": "MOH"
        }
        
        headers = {
            "Content-Type" : "application/json",
            "Authorization": "#apiKey1"
            }
        
        response = self.request(
            method  = 'PUT',
            path    = '/api/club/1',
            headers = headers,
            body    = body
            )

        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['city'], "Mohelnice")
        self.assertEqual(response['country'], "CZE")
        self.assertEqual(response['shortcut'], "MOH")

    def testPut2(self):
        '''change shortcut, city and country by club'''
        body = {
          "city": "Mohelnice",
          "country": "CZE",
          "shortcut": "MOH"
        }
        
        headers = {
            "Content-Type" : "application/json",
            "Authorization": "#apiKey2"
            }
        
        response = self.request(
            method  = 'PUT',
            path    = '/api/club/1',
            headers = headers,
            body    = body
            )

        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['city'], "Mohelnice")
        self.assertEqual(response['country'], "CZE")
        self.assertEqual(response['shortcut'], "MOH")

    def testPut3(self):
        '''change shortcut, city and country by invalid club'''
        body = {
          "city": "Mohelnice",
          "country": "CZE",
          "shortcut": "MOH"
        }
        
        headers = {
            "Content-Type" : "application/json",
            "Authorization": "#apiKey2"
            }
        
        response = self.request(
            method  = 'PUT',
            path    = '/api/club/2',
            headers = headers,
            body    = body
            )

        self.assertEqual(self.srmock.status, HTTP_401)

    def testDelete(self):
        club = models.Club.select().where(models.Club.id == 12).get()
        response = self.request(
            method  = 'DELETE',
            path    = '/api/club/12',
            headers = {
                "Authorization": "#apiKey1"
                }
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        with self.assertRaises(models.Club.DoesNotExist):
            club = models.Club.select().where(models.Club.id == 12).get()  

class ClubPlayers(TestCase):

    def testGet(self):
        players = len(models.Player.select().where(models.Player.clubId == 1))     
        response = self.request(
            method  = 'GET',
            path    = '/api/club/1/players',
            decode  = 'utf-8'
            )
        self.assertEqual(response['count'], players)
        self.assertEqual(self.srmock.status, HTTP_200)

class ClubTeams(TestCase):

    def testGet(self):
        teams = len(models.Team.select().where(models.Team.clubId == 1))     
        response = self.request(
            method  = 'GET',
            path    = '/api/club/1/teams',
            decode  = 'utf-8'
            )
        self.assertEqual(response['count'], teams)
        self.assertEqual(self.srmock.status, HTTP_200)