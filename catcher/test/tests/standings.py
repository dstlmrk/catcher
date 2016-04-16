#!/usr/bin/python
# coding=utf-8

from testCase import TournamentTestCase
from falcon import HTTP_200

class TournamentStandings(TournamentTestCase):

    def testGet1(self):
        '''if all teams are correctly filled in standings before'''
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
      
        response = self.request(
            method  = 'GET',
            path    = ('/api/tournament/%s/standings' % tournamentId),
            headers = {"Content-Type": "application/json"}
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        
        standings = response['standings']
        self.assertEqual(standings[0]['standing'], 1)
        self.assertEqual(standings[1]['standing'], 2)
        self.assertEqual(standings[2]['standing'], 3)
        self.assertEqual(standings[3]['standing'], 4)
        self.assertEqual(standings[0]['teamId'], None)
        self.assertEqual(standings[1]['teamId'], None)
        self.assertEqual(standings[2]['teamId'], None)
        self.assertEqual(standings[3]['teamId'], None)
        self.assertEqual(response['spirits'], None)

    def testGet2(self):
        '''if all teams are correctly filled in standings after terminate tournament'''
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
            headers = {"Content-Type": "application/json"},
            body    = {"terminated": True}
            )
        self.assertEqual(self.srmock.status, HTTP_200)

        response = self.request(
            method  = 'GET',
            path    = ('/api/tournament/%s/standings' % tournamentId),
            headers = {"Content-Type": "application/json"}
            )
        self.assertEqual(self.srmock.status, HTTP_200)

        print response

        standings = response['standings']
        self.assertEqual(standings[0]['standing'], 1)
        self.assertEqual(standings[1]['standing'], 2)
        self.assertEqual(standings[2]['standing'], 3)
        self.assertEqual(standings[3]['standing'], 4)
        self.assertEqual(standings[0]['teamId'], 3)
        self.assertEqual(standings[1]['teamId'], 4)
        self.assertEqual(standings[2]['teamId'], 2)
        self.assertEqual(standings[3]['teamId'], 1)
        self.assertEqual(len(response['spirits']), 4)

        self.assertEqual(response['spirits'][0]['teamId'], 1)
        self.assertEqual(response['spirits'][0]['matches'], 2)
        self.assertEqual(response['spirits'][0]['total'], 12)
        self.assertEqual(response['spirits'][0]['totalGiven'], 10)
        self.assertEqual(response['spirits'][0]['fouls'], 1)
        self.assertEqual(response['spirits'][0]['foulsGiven'], 2)
        self.assertEqual(response['spirits'][0]['fair'], 4)
        self.assertEqual(response['spirits'][0]['fairGiven'], 2)
        self.assertEqual(response['spirits'][0]['communication'], 2)
        self.assertEqual(response['spirits'][0]['communicationGiven'], 2)
        self.assertEqual(response['spirits'][0]['rules'], 3)
        self.assertEqual(response['spirits'][0]['rulesGiven'], 2)
        self.assertEqual(response['spirits'][0]['positive'], 2)
        self.assertEqual(response['spirits'][0]['positiveGiven'], 2)