#!/usr/bin/python
# coding=utf-8

from testCase import TournamentTestCase
from falcon import HTTP_200, HTTP_201, HTTP_400, HTTP_401
from catcher import models

class Group(TournamentTestCase):

    def testPost(self):
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

