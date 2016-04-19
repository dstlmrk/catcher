#!/usr/bin/python
# coding=utf-8

from testCase import TournamentTestCase
from falcon import HTTP_200, HTTP_201, HTTP_304, HTTP_400
from catcher import models

class MissingSpirits(TournamentTestCase):

    def testGet1(self):
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # play all matches on tournament
        self.playMatches(tournamentId)

        # all spirits
        response = self.request(
            method  = 'GET',
            path    = ('/api/tournament/%s/missing-spirits' % tournamentId),
            headers = self.headers
            )

        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['count'], 8)

        matchId = self.getMatchId(tournamentId)
        match = models.Match.get(id=matchId)
        response = self.request(
            method  = 'POST',
            path    = ('/api/match/%s/spirits' % matchId),
            headers = self.headers,
            body    = {
                "teamId": match.awayTeamId,
                "comment": "Game was very agresive, but fair",
                "rules": 4,
                "fouls": 4,
                "fair": 4,
                "positive": 4,
                "communication": 4
                }
            )
        self.assertEqual(self.srmock.status, HTTP_201)

        # all spirits - 1
        response = self.request(
            method  = 'GET',
            path    = ('/api/tournament/%s/missing-spirits' % tournamentId),
            headers = self.headers
            )

        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['count'], 7)

    def testGet2(self):
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # play all matches on tournament
        self.playMatches(tournamentId)
        self.surrenderSpirit(tournamentId)

        response = self.request(
            method  = 'GET',
            path    = ('/api/tournament/%s/missing-spirits' % tournamentId),
            headers = self.headers
            )

        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['count'], 0)

class Spirits(TournamentTestCase):

    def testGet1(self):
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # play all matches on tournament
        self.playMatches(tournamentId)
        self.surrenderSpirit(tournamentId)
        self.terminateTournament(tournamentId)

        response = self.request(
            method  = 'GET',
            path    = ('/api/tournament/%s/spirits' % tournamentId),
            headers = {"Content-Type": "application/json"}
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['count'], 4)

    def testGet2(self):
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # play all matches on tournament
        self.playMatches(tournamentId)
        self.surrenderSpirit(tournamentId)
        self.terminateTournament(tournamentId)
        
        matchId = self.getMatchId(tournamentId)
        match = models.Match.get(id=matchId)
        response = self.request(
            method      = 'GET',
            path        = ('/api/tournament/%s/spirits' % tournamentId),
            headers     = {"Content-Type": "application/json"},
            queryString = ("teamId=%s" % match.homeTeamId)
            )
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['count'], 1)
        print response
        
class Spirit(TournamentTestCase):

    def testGet(self):
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # play all matches on tournament
        self.playMatches(tournamentId)
        self.surrenderSpirit(tournamentId)
        # last match is finale
        match = matches = models.Match.select().where(
            models.Match.tournamentId == tournamentId
            ).order_by(models.Match.startTime.desc())[0]

        # put spirit at final
        response = self.request(
            method  = 'GET',
            path    = ('/api/match/%s' % match.id),
            headers = {"Content-Type": "application/json"}
            )

        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['homeTeam']['spirit'], 12)
        self.assertEqual(response['awayTeam']['spirit'], 10)

        # put spirit at final
        response = self.request(
            method  = 'GET',
            path    = ('/api/match/%s/spirits' % match.id),
            headers = self.headers
            )

        self.assertEqual(self.srmock.status, HTTP_200)

        self.assertEqual(
            response['homeTeam']['spirit']['comment'],
            "Game was very agresive, but fair"
            )
        self.assertEqual(4, response['homeTeam']['spirit']['fair'])
        self.assertEqual(1, response['homeTeam']['spirit']['fouls'])
        self.assertEqual(2, response['homeTeam']['spirit']['positive'])
        self.assertEqual(3, response['homeTeam']['spirit']['rules'])
        self.assertEqual(2, response['homeTeam']['spirit']['communication'])
        self.assertEqual(12, response['homeTeam']['spirit']['total'])

        self.assertEqual(
            response['awayTeam']['spirit']['comment'],
            "Game was very agresive, but fair"
            )
        self.assertEqual(2, response['awayTeam']['spirit']['fair'])
        self.assertEqual(2, response['awayTeam']['spirit']['fouls'])
        self.assertEqual(2, response['awayTeam']['spirit']['positive'])
        self.assertEqual(2, response['awayTeam']['spirit']['rules'])
        self.assertEqual(2, response['awayTeam']['spirit']['communication'])
        self.assertEqual(10, response['awayTeam']['spirit']['total'])

    def testPost(self):
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # play all matches on tournament
        self.playMatches(tournamentId)
        self.surrenderSpirit(tournamentId)
        # last match is finale
        match = matches = models.Match.select().where(
            models.Match.tournamentId == tournamentId
            ).order_by(models.Match.startTime.desc())[0]

        # finale receiving table for team, which has two average spirits
        spiritAvg = models.SpiritAvg.get(
            tournamentId = tournamentId,
            teamId = match.awayTeamId
            )
        self.assertEqual(2, spiritAvg.matches)
        self.assertEqual(2, spiritAvg.communication)
        self.assertEqual(2, spiritAvg.fair)
        self.assertEqual(2, spiritAvg.fouls)
        self.assertEqual(2, spiritAvg.positive)
        self.assertEqual(2, spiritAvg.rules)
        self.assertEqual(10, spiritAvg.total)

        # finale receiving table for team, which has two different spirits
        spiritAvg = models.SpiritAvg.get(
            tournamentId = tournamentId,
            teamId = match.homeTeamId
            )
        self.assertEqual(2, spiritAvg.matches)
        self.assertEqual(2, spiritAvg.communication)
        self.assertEqual(3, spiritAvg.fair)
        self.assertEqual(1.5, spiritAvg.fouls)
        self.assertEqual(2, spiritAvg.positive)
        self.assertEqual(2.5, spiritAvg.rules)
        self.assertEqual(11, spiritAvg.total)

        # finale giving table for team, which has two average spirits
        spiritAvg = models.SpiritAvg.get(
            tournamentId = tournamentId,
            teamId = match.awayTeamId
            )
        self.assertEqual(2, spiritAvg.matchesGiven)
        self.assertEqual(2, spiritAvg.communicationGiven)
        self.assertEqual(4, spiritAvg.fairGiven)
        self.assertEqual(1, spiritAvg.foulsGiven)
        self.assertEqual(2, spiritAvg.positiveGiven)
        self.assertEqual(3, spiritAvg.rulesGiven)
        self.assertEqual(12, spiritAvg.totalGiven)

        # finale giving table for team, which has two different spirits
        spiritAvg = models.SpiritAvg.get(
            tournamentId = tournamentId,
            teamId = match.homeTeamId
            )
        self.assertEqual(2, spiritAvg.matchesGiven)
        self.assertEqual(2, spiritAvg.communicationGiven)
        self.assertEqual(3, spiritAvg.fairGiven)
        self.assertEqual(1.5, spiritAvg.foulsGiven)
        self.assertEqual(2, spiritAvg.positiveGiven)
        self.assertEqual(2.5, spiritAvg.rulesGiven)
        self.assertEqual(11, spiritAvg.totalGiven)

    def testPut(self):
        newTournament = self.createTournament()
        tournamentId = newTournament['id']
        # ready tournament
        self.readyTournament(tournamentId)
        self.createRosters(tournamentId)
        # play all matches on tournament
        self.playMatches(tournamentId)
        self.surrenderSpirit(tournamentId)
        # last match is finale
        match = matches = models.Match.select().where(
            models.Match.tournamentId == tournamentId
            ).order_by(models.Match.startTime.desc())[0]

        # put spirit at final
        response = self.request(
            method  = 'PUT',
            path    = ('/api/match/%s/spirits' % match.id),
            headers = self.headers,
            body    = {
                "teamId": match.homeTeamId,
                "comment": "Game was very agresive, but fair",
                "rules": 4,
                "fouls": 0,
                "fair": 4,
                "positive": 3,
                "communication": 3
                }
            )

        self.assertEqual(self.srmock.status, HTTP_200)

        # put spirit at final
        response = self.request(
            method  = 'PUT',
            path    = ('/api/match/%s/spirits' % match.id),
            headers = self.headers,
            body    = {
                "teamId": match.awayTeamId,
                "comment": "Game was very agresive, but fair",
                "rules": 4,
                "fouls": 4,
                "fair": 4,
                "positive": 4,
                "communication": 4
                }
            )

        self.assertEqual(self.srmock.status, HTTP_200)

        # finale receiving table for team, which has two average spirits
        spiritAvg = models.SpiritAvg.get(
            tournamentId = tournamentId,
            teamId = match.awayTeamId
            )
        self.assertEqual(2, spiritAvg.matches)
        self.assertEqual(3, spiritAvg.communication)
        self.assertEqual(3, spiritAvg.fair)
        self.assertEqual(3, spiritAvg.fouls)
        self.assertEqual(3, spiritAvg.positive)
        self.assertEqual(3, spiritAvg.rules)
        self.assertEqual(15, spiritAvg.total)

        # finale receiving table for team, which has two different spirits
        spiritAvg = models.SpiritAvg.get(
            tournamentId = tournamentId,
            teamId = match.homeTeamId
            )
        self.assertEqual(2, spiritAvg.matches)
        self.assertEqual(2.5, spiritAvg.communication)
        self.assertEqual(3, spiritAvg.fair)
        self.assertEqual(1, spiritAvg.fouls)
        self.assertEqual(2.5, spiritAvg.positive)
        self.assertEqual(3, spiritAvg.rules)
        self.assertEqual(12, spiritAvg.total)

        # finale giving table for team, which has two average spirits
        spiritAvg = models.SpiritAvg.get(
            tournamentId = tournamentId,
            teamId = match.awayTeamId
            )
        self.assertEqual(2, spiritAvg.matchesGiven)
        self.assertEqual(2.5, spiritAvg.communicationGiven)
        self.assertEqual(4, spiritAvg.fairGiven)
        self.assertEqual(0.5, spiritAvg.foulsGiven)
        self.assertEqual(2.5, spiritAvg.positiveGiven)
        self.assertEqual(3.5, spiritAvg.rulesGiven)
        self.assertEqual(13, spiritAvg.totalGiven)

        # finale giving table for team, which has two different spirits
        spiritAvg = models.SpiritAvg.get(
            tournamentId = tournamentId,
            teamId = match.homeTeamId
            )
        self.assertEqual(2, spiritAvg.matchesGiven)
        self.assertEqual(3, spiritAvg.communicationGiven)
        self.assertEqual(4, spiritAvg.fairGiven)
        self.assertEqual(2.5, spiritAvg.foulsGiven)
        self.assertEqual(3, spiritAvg.positiveGiven)
        self.assertEqual(3.5, spiritAvg.rulesGiven)
        self.assertEqual(16, spiritAvg.totalGiven)
