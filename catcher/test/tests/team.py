#!/usr/bin/python
# coding=utf-8

import falcon
import pytest


def test_team_get(client, models, users):
    team_id = models.Team.insert(
        division=1, name="Frozen Angels", shortcut="FAL",
        city="Liberec", country="CZE", user_id=1,
    ).execute()
    resp = client.get('/api/team/%s' % team_id)
    expected_resp = {
        'id': team_id,
        'name': 'Frozen Angels',
        'cald_id': None,
        'country': 'CZE',
        'shortcut': 'FAL',
        'city': 'Liberec',
        'user_id': 1,
        'division': {
            'division': 'open',
            'id': 1
        }
    }
    print resp.json
    assert resp.status == falcon.HTTP_OK
    assert resp.json == expected_resp


def test_teams_get(client, teams):
    resp = client.get('/api/teams')
    assert resp.status == falcon.HTTP_OK
    assert len(resp.json['teams']) == 3
    assert resp.json['teams'][0]['name'] == "Frozen Angels"
    assert resp.json['teams'][1]['country'] == "SVK"
    assert resp.json['teams'][1]['cald_id'] == None
    assert resp.json['teams'][2]['division']['division'] == "women"
    assert resp.json['teams'][2]['city'] == u"Plzeň"


def test_specific_teams_get(client, teams):
    resp = client.get('/api/teams?city=Liberec&country=CZE')
    print resp.json
    assert resp.status == falcon.HTTP_OK
    assert len(resp.json['teams']) == 1
    assert resp.json['teams'][0]['name'] == "Frozen Angels"
    assert resp.json['teams'][1]['country'] == "CZE"


def test_specific_teams_get(client, teams):
    resp = client.get('/api/teams?division_id=2')
    print resp.json
    assert resp.status == falcon.HTTP_OK
    assert len(resp.json['teams']) == 2
    assert resp.json['teams'][0]['division']['id'] == 2


#     def testPost1(self):
#         body = {
#             "clubId": 12,
#             "degree": "A",
#             "divisionId": 2
#             }
#         headers = {
#             "Content-Type" : "application/json",
#             "Authorization": "#apiKey1"
#             }
#         response = self.request(
#             method  = 'POST',
#             path    = '/api/teams',
#             headers = headers,
#             body    = body
#             )

#         expectedResponse = {
#             "clubId": 12,
#             "degree": "A",
#             "divisionId": 2
#             }

#         # I can't know, what id is there
#         del response['id']
#         self.assertEqual(response, expectedResponse)
#         self.assertEqual(self.srmock.status, HTTP_201)

#     def testPost2(self):
#         '''create team with unvalid club id'''
#         body = {
#             "clubId": 999999,
#             "degree": "A",
#             "divisionId": 2
#             }
#         headers = {
#             "Content-Type" : "application/json",
#             "Authorization": "#apiKey1"
#             }
#         response = self.request(
#             method  = 'POST',
#             path    = '/api/teams',
#             headers = headers,
#             body    = body
#             )
#         expectedResponse = {
#             "clubId": 12,
#             "degree": "A",
#             "divisionId": 2
#             }
#         self.assertEqual(self.srmock.status, HTTP_400)

# class Team(TestCase):

#     def testGet(self):
#         team = models.Team.select().where(models.Team.id == 1).get()        
#         club = models.Club.select().where(models.Club.id == team.clubId).get()
#         name = club.name + " " + team.degree
#         response = self.request(
#             method  = 'GET',
#             path    = '/api/team/1',
#             decode  = 'utf-8'
#             )
#         self.assertEqual(response['id'], team.id)
#         self.assertEqual(response['clubId'], team.clubId)
#         self.assertEqual(response['degree'], team.degree)
#         self.assertEqual(response['divisionId'], team.divisionId)
#         self.assertEqual(response['name'], name)
#         self.assertEqual(self.srmock.status, HTTP_200)

#     def testPut(self):
#         '''change shortcut, city and country'''
#         body = {
#           "degree": 'B',
#           "divisionId": 4
#         }
        
#         headers = {
#             "Content-Type" : "application/json",
#             "Authorization": "#apiKey1"
#             }
        
#         response = self.request(
#             method  = 'PUT',
#             path    = '/api/team/16',
#             headers = headers,
#             body    = body
#             )

#         self.assertEqual(self.srmock.status, HTTP_200)
#         self.assertEqual(response['degree'], 'B')
#         self.assertEqual(response['divisionId'], 4)

#     def testDelete(self):
#         club = models.Team.select().where(models.Team.id == 15).get()
#         response = self.request(
#             method  = 'DELETE',
#             path    = '/api/team/15',
#             headers = {
#                 "Authorization": "#apiKey1"
#                 }
#             )
#         self.assertEqual(self.srmock.status, HTTP_200)
#         with self.assertRaises(models.Team.DoesNotExist):
#             club = models.Team.select().where(models.Team.id == 15).get()