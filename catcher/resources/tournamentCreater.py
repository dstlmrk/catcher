#!/usr/bin/python
# coding=utf-8

import models as m
from datetime import datetime
import falcon

class TournamentCreater(object):

    def getTimestamp(self, timestamp):
        try:
            return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return datetime.strptime(timestamp, "%Y-%m-%d")

    def checkTeams(self, teams, divisionId):
        seeding = set()
        teamIds = set()
        teamsCount = len(teams)
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

    def checkFields(self, fields):
        fieldIds = set()
        fieldsCount = len(fields)
        if fieldsCount == 0:
            raise ValueError("Tournament without fields is not allowed")
        for field in fields:
            fieldIds.add(field['id'])
        # check, if all fields are added only once
        if len(fieldIds) != fieldsCount:
            raise ValueError("Some field is added more times than once")

    def checkMatchId(self, id):
        if not isinstance(id, str) and not isinstance(id, unicode):
            raise ValueError(
                "Match %s must be string, but it's %s" % (id, type(id))
                )
        if not 0 < len(id) <= 3:
            raise ValueError(
                "Match %s must have structure from one to three characters" % id 
                )
        if not any(c.isalpha() for c in id):
            raise ValueError(
                "Match %s must have alphanumeric structure" % id
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
                                "Match %s is starting during"
                                " match %s on the same field" \
                                % (match[0], otherMatch[0])
                                )
                        # check, if match isn't ending during other matches 
                        if otherMatch[1] <= match[2] <= otherMatch[2]:
                            raise ValueError(
                                "Match %s is ending during"
                                " match %s on the same field" \
                                % (match[0], otherMatch[0])
                                )

    def checkTimesAndFields(self, matches, startDate, endDate, fields):
        fieldIds = set(field['id'] for field in fields)
        # set dict of games for each field
        schedule = dict((field['id'], []) for field in fields)
        # check, if all games in tournament term and times are correct
        for match in matches:
            startTime = self.getTimestamp(match['startTime'])
            endTime   = self.getTimestamp(match['endTime'])
            if startTime > endTime:
                raise ValueError(
                    "Match %s has incorrect time"
                    " (start is after end)" % match['identificator']
                    )
            if startDate.date() > startTime.date() or endTime.date() > endDate.date():
                raise ValueError(
                    "Match %s has incorrect time"
                    " (isn't in the tournament term)" % match['identificator']
                    )
            # on the field is added match
            schedule[match['field']].append(
                (match['identificator'], startTime, endTime)
                )
        self.checkMatchTimes(schedule)

    def checkMatchIds(self, match):
        # matchId can be only alphanumeric (no int)
        self.checkMatchId(match['identificator'])
        # check ids in play-off, it can be alphanumeric
        if match['winnerNextStep']:
            self.checkMatchId(match['winnerNextStep'])
        if match['looserNextStep']:
            self.checkMatchId(match['looserNextStep'])

    def checkMatches(self, matches, startDate, endDate, fields):
        matchIds = set()
        matchesCount = len(matches)
        if matchesCount == 0:
            raise ValueError("Tournament without matches is not allowed")
        for match in matches:
            self.checkMatchIds(match)
            matchIds.add(match['identificator'])
            # check, if exists way further
            if not match.get('looserNextStep') and not match.get('looserFinalStanding'):
                raise ValueError(
                    "Match %s has no more way for looser" % match['identificator']
                    )
            if not match.get('winnerNextStep') and not match.get('winnerFinalStanding'):
                raise ValueError(
                    "Match %s has no more way for winner" % match['identificator']
                    )

        # check, if all matches are added only once
        if len(matchIds) != matchesCount:
            raise ValueError("Some match is added more times than once")
        self.checkTimesAndFields(matches, startDate, endDate, fields)

    def checkSeedings(self, matches, teamsCount):
        for match in matches:
            homeSeed = match.get('homeSeed')
            awaySeed = match.get('awaySeed')
            # check, if it's play-off game
            if homeSeed is None and awaySeed is None:
                continue
            # check, if seedings are out of range
            if homeSeed is not None and not 1 <= homeSeed <= teamsCount:
                raise ValueError(
                    "Match %s has seeding home team out of range" % match['identificator']
                    )
            if awaySeed is not None and not 1 <= awaySeed <= teamsCount:
                raise ValueError(
                    "Match %s has seeding away team out of range" % match['identificator']
                    )
            # check, if seeding are equal
            if homeSeed == awaySeed:
                raise ValueError("Match %s has two same teams" % match['identificator'])

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
            matchId = match['identificator']
            winnerFinalStanding  = match.get('winnerFinalStanding')
            looserFinalStanding  = match.get('looserFinalStanding')

            # check final statements
            if winnerFinalStanding:
                if not 1 <= winnerFinalStanding <= len(matches):
                    raise ValueError(
                        "Final statement %s is out of range" \
                        % winnerFinalStanding
                        )
                try:
                    finalPlacements.remove(winnerFinalStanding)
                except ValueError:
                    raise ValueError(
                        "Final statement %s is contained more than once" \
                        % winnerFinalStanding
                        )
            if looserFinalStanding:
                if not 1 <= looserFinalStanding <= len(matches):
                    raise ValueError(
                        "Final statement %s is out of range" \
                        % looserFinalStanding
                        )
                try:
                    finalPlacements.remove(looserFinalStanding)
                except ValueError:
                    raise ValueError(
                        "Final statement %s is contained more than once" \
                        % looserFinalStanding
                        )

            # check deadlock
            if winnerFinalStanding == matchId or looserFinalStanding == matchId:
                raise ValueError("Match %s has infinite loop for next process" % matchId)

        # final check, if all final statements are used
        if len(finalPlacements) != 0:
            raise ValueError("Final placements %s are not reachable" % finalPlacements)

        # check, if all games have only two ways inwards
        processes  = []
        for match in matches:
            if match['winnerNextStep']:
                processes.append(match['winnerNextStep'])
            if match['looserNextStep']:
                processes.append(match['looserNextStep'])

        for match in matches:
            # TODO: az budu kontrolovat i skupiny, musim je zde vyradit
            matchId = match['identificator']
            # if teams aren't seeded, way inwards must be here
            if not match['homeSeed'] or not match['awaySeed']:
                try:
                    # twice removed because there have to be two ways  
                    processes.remove(matchId)
                    processes.remove(matchId)
                except ValueError:
                    raise ValueError("In match %s won't play two teams" % matchId)

        # TODO: napsat funkce pro simulaci pruchodu turnajem, aby se zjistilo,
        # ze nejaky tym nema sanci skoncit prvni (druhy apod.)

        # TODO: popremyslet nad sofistikovanejsi kontrolou turnaje
        # (1) --+ (FIN) +-- (SE1)
        # (2) --/       \-- (SE2)

        # (3) --+ (3RD) +-- (SE1)
        # (4) --/       \-- (SE2)

    @m.db.atomic()
    def saveTournament(self, data):
        print "UKLADAM"

        print data['endDate']
        # Tournament
        tournamentId = m.Tournament.insert(
            caldTournament   = data.get('caldTournament'),
            city             = data.get('city'),
            country          = data.get('country'),
            division         = data['division'],
            name             = data['name'],
            startDate        = data['startDate'],
            endDate          = data['endDate'],
            teams            = len(data['teams']),
            active           = False,
            terminated       = False
            ).execute()

        # Field
        for field in data['fields']:
            m.Field.insert(tournament = tournamentId, **field).execute()

        # TeamAtTournament
        for team in data['teams']:
            m.TeamAtTournament.insert(
                team       = team['id'],
                seeding    = team['seeding'],
                tournament = tournamentId
                ).execute()

        for match in data['matches']:
            
            # Identificators
            identificator, created = m.Identificator.get_or_create(
                tournament    = tournamentId,
                identificator = match['identificator']
                )

            winnerNextStep = None
            if match['winnerNextStep'] is not None:
                winnerNextStep, created = m.Identificator.get_or_create(
                    tournament    = tournamentId,
                    identificator = match['winnerNextStep']
                    )

            looserNextStep = None
            if match['looserNextStep'] is not None:
                looserNextStep, created = m.Identificator.get_or_create(
                    tournament    = tournamentId,
                    identificator = match['looserNextStep']
                    )

            del match['identificator']
            del match['winnerNextStep']
            del match['looserNextStep']

            # Match
            matchId = m.Match.insert(
                tournament = tournamentId,
                identificator = identificator.id,
                terminated = False,
                looserNextStep = looserNextStep,
                winnerNextStep = winnerNextStep,
                **match
                ).execute()

            m.Identificator.\
                update(matchId = matchId).\
                where(m.Identificator.id == identificator.id).\
                execute()

        return tournamentId

    # method get is used, where value can be null
    def createTournament(self, req, resp):
        data = req.context['data']

        # load term and check it
        startDate = self.getTimestamp(data['startDate'])
        endDate   = self.getTimestamp(data['endDate'])
        if startDate.date() > endDate.date():
            raise ValueError("Tournament has incorrect term (from is after to)")
        
        # check, if division exists
        divisionId = data['division']
        m.Division.get(m.Division.id == divisionId)

        # load and check teams
        teams = data.get('teams')
        self.checkTeams(teams, divisionId)

        # load and check fields
        fields = data.get('fields')
        self.checkFields(fields)
        
        # load groups
        # TODO: nacist a zkontrolovat skupiny

        # load and check matches
        matches = data.get('matches')
        # TODO: nutne otestovat
        self.checkSeedings(matches, len(teams))
        self.checkMatches(matches, startDate, endDate, fields)
        self.checkTournamentTree(matches, teams)
 
        # atomic create tournament
        tournamentId = self.saveTournament(data)

        # for result body
        createdTurnament = m.Tournament.get(id=tournamentId)

        return createdTurnament