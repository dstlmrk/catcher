#!/usr/bin/python
# coding=utf-8

from catcher.resource import Collection, Item
from catcher import models as m

class Tournament(Item):
    pass

class Tournaments(Collection):
    pass

class CreateTournament(object):

    def checkTeams(self, teams, teamsCount, divisionId):
        seeding = set()
        teamIds = set()
        if len(teams) != teamsCount:
            raise ValueError("Number of teams does not match")
        if teamsCount == 0:
            raise ValueError("Tournament without teams is not allowed")
        for team in teams:
            teamIds.add(team['id'])
            seeding.add(team['seeding'])
            # check, if team exists
            dbTeam = m.Team.select().where(m.Team.id == team['id']).get()
            # check, if team is in correct divison
            if dbTeam.division_id != divisionId:
                raise ValueError("Team with id %s is in incorrect division" % team['id'])
        # check, if set of seeds does match the correct set of seeds
        if seeding != set([x for x in range(1, teamsCount + 1)]):
            raise ValueError("Seeding of teams does not match")
        # check, if all teams are added only once
        if len(teamIds) != teamsCount:
            raise ValueError("Some team is added more times than once")

    def checkFields(self, fields, fieldsCount):
        fieldIds = set()
        if len(fields) != fieldsCount:
            raise ValueError("Number of fields does not match")
        if fieldsCount == 0:
            raise ValueError("Tournament without fields is not allowed")
        for field in fields:
            fieldIds.add(field['id'])
        # check, if all fields are added only once
        if len(fieldIds) != fieldsCount:
            raise ValueError("Some field is added more times than once")

    def checkMatchId(self, id):
        if not isinstance(id, str):
            raise ValueError("Id of match must be string, but it's %s" % type(id))
        if not 0 < len(id) <= 3:
            raise ValueError("Id of match must have structure from one to three characters")
        if not any(c.isalpha() for c in id):
            raise ValueError("Id of match must have alphanumeric (no numbers only) structure")
        return id

    def checkMatchTimes(self, matches, datetimeFrom, dateTimeTo, fields):
        pass

    def checkMatches(self, matches, matchesCount, datetimeFrom, dateTimeTo, fields):
        matchIds = set()
        fieldIds = set(field['id'] for field in fields)
        print fieldIds
        if len(matches) != matchesCount:
            raise ValueError("Number of matches does not match")
        if matchesCount == 0:
            raise ValueError("Tournament without matches is not allowed")
        for match in matches:
            matchIds.add(self.checkMatchId(match['matchId']))
        # check, if all matches are added only once
        if len(matchIds) != matchesCount:
            raise ValueError("Some match is added more times than once")

        self.checkMatchTimes(matches, datetimeFrom, dateTimeTo, fields)


    # method get is used if value can be null
    def on_post(self, req, resp):
        data = req.context['data']

        # base data
        tournamentName = data['name']
        city = data.get('city')
        country = data.get('country')
        caldTournamentId = data.get('caldTournamentId')

        # load time for control
        datetimeFrom = data['datetimeFrom']
        dateTimeTo = data['dateTimeTo']
        
        # check, if division exists
        divisionId = data['divisionId']
        m.Division.get(m.Division.id == divisionId)

        # load and check teams
        teamsCount = data['teamsCount']
        teams      = data.get('teams')
        self.checkTeams(teams, teamsCount, divisionId)

        # load and check fields
        fieldsCount = data['fieldsCount']
        fields      = data.get('fields')
        self.checkFields(fields, fieldsCount)
        
        # load groups
        # TODO: nacist a zkontrolovat skupiny

        # load matches
        matchesCount = data['matchesCount']
        matches      = data.get('matches')
        self.checkMatches(matches, matchesCount, datetimeFrom, dateTimeTo, fields)

        # TODO: cela operace zapisovani do DB musi byt ATOMICKA
        req.context['result'] = tournamentName