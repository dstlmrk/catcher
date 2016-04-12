#!/usr/bin/python
# coding=utf-8

from falcon import HTTP_200, HTTP_400
from tournament import TournamentTestCase
from catcher import models

class Match(TournamentTestCase):

    def testGet(self):
        newTournament = self.createTournament()
        # get one id match
        match = models.Match.select().where(
            models.Match.tournamentId == newTournament['id']
            )[0]
        response = self.request(
            method  = 'GET',
            path    = ('/api/match/%s' % match.id)
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(match.id, response['id'])

    def testPutActive(self):
        pass
        # TODO: testovat, pokud bude zmena atributu active neco delat

    def testPutTerminate(self):
        pass
        # TODO: testovat, pokud bude zmena atributu terminate neco delat

    def testPut1(self):
        newTournament = self.createTournament()
        # get one id match
        match = models.Match.select().where(
            models.Match.tournamentId == newTournament['id']
            )[0]
        response = self.request(
            method  = 'PUT',
            path    = ('/api/match/%s' % match.id),
            headers = {"Content-Type": "application/json"},
            body    = {"description": "Baráž"}
            )
        print response

    def testPut2(self):
        '''unvalid fieldId'''
        newTournament = self.createTournament()
        # get one id match
        match = models.Match.select().where(
            models.Match.tournamentId == newTournament['id']
            )[0]
        response = self.request(
            method  = 'PUT',
            path    = ('/api/match/%s' % match.id),
            headers = {"Content-Type": "application/json"},
            body    = {"fieldId": 2}
            )
        self.assertEqual(self.srmock.status, HTTP_400)

class MatchPoints(TournamentTestCase):
    pass
    # TODO: dokoncit