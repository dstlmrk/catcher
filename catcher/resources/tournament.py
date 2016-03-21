#!/usr/bin/python
# coding=utf-8

from catcher.resource import Collection, Item
from catcher import models as m
from datetime import datetime

class Tournament(Item):
    pass

class Tournaments(Collection):
    pass

class CreateTournament(object):

    def isFinalPlacement(self, id):
        return True if isinstance(id, int) else False

    def getTimestamp(self, timestamp):
        try:
            return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return datetime.strptime(timestamp, "%Y-%m-%d")

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
                raise ValueError("Team %s is in incorrect division" % team['id'])
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
            raise ValueError(
                "Match id (%s) must be string (only final statement can be int)," \
                " but it's %s" % (id, type(id))
                )
        if not 0 < len(id) <= 3:
            raise ValueError(
                "Match id (%s) must have structure from one to three characters" \
                % id 
                )
        if not any(c.isalpha() for c in id):
            raise ValueError(
                "Match id (%s) must have alphanumeric (no numbers only) structure" \
                % id
                )

    def checkMatchTimes(self, schedule):
        for matches in schedule.itervalues():
            for match in matches:
                # compare with other matches
                for otherMatch in matches:
                    # doesn't check itsefl
                    if otherMatch != match:
                        if otherMatch[1] <= match[1] <= otherMatch[2]:
                            raise ValueError(
                                "Match %s is starting during match %s on the same field" \
                                % (match[0], otherMatch[0])
                                )
                        # check, if match isn't ending during other matches 
                        if otherMatch[1] <= match[2] <= otherMatch[2]:
                            raise ValueError(
                                "Match %s is ending during match %s on the same field" \
                                % (match[0], otherMatch[0])
                                )

    def checkTimesAndFields(self, matches, datetimeFrom, datetimeTo, fields):
        fieldIds = set(field['id'] for field in fields)
        # set dict of games for each field
        schedule = dict((field['id'], []) for field in fields)
        # check, if all games in tournament term and times are correct
        for match in matches:
            timeFrom = self.getTimestamp(match['timeFrom'])
            timeTo   = self.getTimestamp(match['timeTo'])
            if timeFrom > timeTo:
                raise ValueError(
                    "Match %s has incorrect time (from is after to)" % match['id']
                    )
            if datetimeTo.date() > timeFrom.date() or timeTo.date() > datetimeTo.date():
                raise ValueError(
                    "Match %s has incorrect time (isn't in the tournament term)" \
                    % match['id']
                    )
            # on the field is added match
            schedule[match['fieldId']].append((match['id'], timeFrom, timeTo))
        self.checkMatchTimes(schedule)

    def checkMatchIds(self, match):
        # check match id
        matchId = match.get('id')
        # matchId can be only alphanumeric (no int)
        self.checkMatchId(matchId)
        # check ids in play-off, it can be alphanumeric or int (final statement)
        try:
            winner = match['winner']
            self.checkMatchId(winner)
        except ValueError:
            if not self.isFinalPlacement(winner):
                raise ValueError("Match %s has incorrect winner" % matchId)
        try:
            looser = match['looser']
            self.checkMatchId(looser)
        except ValueError:
            if not self.isFinalPlacement(looser):
                raise ValueError("Match %s has incorrect looser" % matchId)

    def checkMatches(self, matches, matchesCount, datetimeFrom, datetimeTo, fields):
        matchIds = set()
        if len(matches) != matchesCount:
            raise ValueError("Number of matches does not match")
        if matchesCount == 0:
            raise ValueError("Tournament without matches is not allowed")
        for match in matches:
            self.checkMatchIds(match)
            matchIds.add(match['id'])
        # check, if all matches are added only once
        if len(matchIds) != matchesCount:
            raise ValueError("Some match is added more times than once")
        self.checkTimesAndFields(matches, datetimeFrom, datetimeTo, fields)

    def checkSeedings(self, matches, teamsCount):
        for match in matches:
            seedingHome = match.get('seedingHome')
            seedingAway = match.get('seedingAway')
            # check, if it's play-off game
            if seedingHome is None and seedingAway is None:
                continue
            # check, if seedings are out of range
            if seedingHome is not None and not 1 <= seedingHome <= teamsCount:
                raise ValueError(
                    "Match %s has seeding home team out of range" % match['id']
                    )
            if seedingAway is not None and not 1 <= seedingAway <= teamsCount:
                raise ValueError(
                    "Match %s has seeding away team out of range" % match['id']
                    )
            # check, if seeding are equal
            if seedingHome == seedingAway:
                raise ValueError("Match %s has two same teams" % match['id'])

    class Match(object):
        def __init__(self, id, winMatch=None, lostMatch=None, placement=None):
            self.id        = id
            self.winMatch  = winMatch
            self.lostMatch = lostMatch
            self.placement = placement
            self.freeSpots = 2

    def checkTournamentTree(self, matches, teams):
        finalPlacements = list([x for x in range(1, len(teams) + 1)])

        for match in matches:
            matchId = match['id']
            winner  = match['winner']
            looser  = match['looser']

            # if it's match with final statements, it will be saved
            if self.isFinalPlacement(winner):
                if not 1 <= winner <= len(matches):
                    raise ValueError("Final statement %s is out of range" % winner)
                try:
                    finalPlacements.remove(winner)
                except ValueError:
                    raise ValueError("Final statement %s is contained more than once" % winner)

            if self.isFinalPlacement(looser):
                if not 1 <= looser <= len(matches):
                    raise ValueError("Final statement %s is out of range" % looser)
                try:
                    finalPlacements.remove(looser)
                except ValueError:
                    raise ValueError("Final statement %s is contained more than once" % looser)

            # check deadlock
            if winner == matchId or looser == matchId:
                raise ValueError("Match %s has infinite loop for next process" % matchId)

        # final check, if all final statements are used
        if len(finalPlacements) != 0:
            raise ValueError("Final placements %s are not reachable" % finalPlacements)

        # udelat strom playoff, kde nahore budou rodice
        # s umistenim a pod nim se budou vetvit zapasy

        # 1 --+ FIN +-- SE1
        # 2 --/     \-- SE2

        # 3 --+ 3RD +-- SE1
        # 4 --/     \-- SE2

        # {
        # "fieldId": 1,
        # "timeFrom": "2016-04-01T09:00:00",
        # "timeTo": "2016-04-01T09:29:00",
        # "seedingHome": 1,
        # "seedingAway": 4,
        # "winner": "FIN",
        # "looser": "3RD",
        # "matchId": "SE1"
        # }

    # method get is used if value can be null
    def on_post(self, req, resp):

        data = req.context['data']

        # TODO: mel bych cele projet a zkontrolovat, zda sedi datove typy a nejake hodnoty nechybi,
        # bez jakkekoliv dalsi logiky

        # base data
        tournamentName   = data['name']
        city             = data.get('city')
        country          = data.get('country')
        caldTournamentId = data.get('caldTournamentId')

        # load term and check it
        datetimeFrom = self.getTimestamp(data['datetimeFrom'])
        datetimeTo   = self.getTimestamp(data['datetimeTo'])
        if datetimeFrom.date() > datetimeTo.date():
            raise ValueError("Tournament has incorrect term (from is after to)")
        
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

        # load and check matches
        matchesCount = data['matchesCount']
        matches      = data.get('matches')
        # TODO: nutne otestovat
        self.checkSeedings(matches, teamsCount)
        self.checkMatches(matches, matchesCount, datetimeFrom, datetimeTo, fields)
        self.checkTournamentTree(matches, teams)

        # TODO: cela operace zapisovani do DB musi byt ATOMICKA

        req.context['result'] = tournamentName