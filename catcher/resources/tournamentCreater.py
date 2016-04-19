#!/usr/bin/python
# coding=utf-8

from catcher import models as m
from datetime import datetime
import falcon

# TODO: kdyz zadam u finale homeSeed, turnaj se vytvori

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
            if dbTeam.divisionId != divisionId:
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

    def checkGroups(self, groups):
        # TODO: write better input control
        if not groups:
            return
        
        for group in groups:
            teamsCount = len(group['teams'])

            if teamsCount <= 0:
                raise ValueError("Group without teams is not allowed")

            if teamsCount != len(group['advancements']):
                raise ValueError("Number of teams and advancements don't correspond")

            advancements = set([x for x in range(1, teamsCount + 1)])
            for advancement in group['advancements']:
                advancements.remove(advancement['standing'])
                if advancement.get('nextStep') is None and advancement.get('finalStanding') is None:
                    raise ValueError(
                        "Advancement for %s.place in group %s is missing"
                        % (advancement['standing'], group['ide'])
                        )
            
            if len(advancements) != 0:
                raise ValueError("Some advancements in group %s are missing" % group['ide'])

            # for future use
            # matchesInGroup = [
            #     match for match in matches if match['ide']==group['ide']
            #     ]

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
                    " (start is after end)" % match['ide']
                    )
            if startDate.date() > startTime.date() or endTime.date() > endDate.date():
                raise ValueError(
                    "Match %s has incorrect time"
                    " (isn't in the tournament term)" % match['ide']
                    )
            # on the field is added match
            schedule[match['fieldId']].append(
                (match['ide'], startTime, endTime)
                )
        self.checkMatchTimes(schedule)

    def checkMatchIds(self, match):
        # matchId can be only alphanumeric (no int)
        self.checkMatchId(match['ide'])
        # check ids in play-off, it can be alphanumeric
        if match['winnerNextStepIde']:
            self.checkMatchId(match['winnerNextStepIde'])
        if match['looserNextStepIde']:
            self.checkMatchId(match['looserNextStepIde'])

    @staticmethod
    def checkNextStepInMatch(match):
        if not match.get('looserNextStepIde') and not match.get('looserFinalStanding'):
            raise ValueError(
                    "Match %s has no more way for looser" % match['ide']
                    )
        if not match.get('winnerNextStepIde') and not match.get('winnerFinalStanding'):
            raise ValueError(
                "Match %s has no more way for winner" % match['ide']
                )

    def checkMatches(self, matches, startDate, endDate, fields, groups):
        groupMatches = []
        groupIdentificators = [group['ide'] for group in groups]
        print groupIdentificators
        matchIds = set()
        # matchesCount = len(matches)
        if len(matches) == 0:
            raise ValueError("Tournament without matches is not allowed")
        for match in matches:
            self.checkMatchIds(match)
            # if match isn't in group check, if exists way further
            if match['ide'] not in groupIdentificators:
                matchIds.add(match['ide'])
                TournamentCreater.checkNextStepInMatch(match)
            else:
                groupMatches.append(match)

        # check, if all matches are added only once
        # if len(matchIds) != matchesCount:
        #     raise ValueError("Some match is added more times than once")
        self.checkTimesAndFields(matches, startDate, endDate, fields)

        return groupMatches

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
                    "Match %s has seeding home team out of range" % match['ide']
                    )
            if awaySeed is not None and not 1 <= awaySeed <= teamsCount:
                raise ValueError(
                    "Match %s has seeding away team out of range" % match['ide']
                    )
            # check, if seeding are equal
            if homeSeed == awaySeed:
                raise ValueError("Match %s has two same teams" % match['ide'])

    class Match(object):
        def __init__(self, id, winMatch=None, lostMatch=None, placement=None):
            self.id        = id
            self.winMatch  = winMatch
            self.lostMatch = lostMatch
            self.placement = placement
            self.freeSpots = 2

    def checkFinalPlacementRange(self, placement, placementsCount):
        if not 1 <= placement <= placementsCount:
            raise ValueError(
                "Final statement %s is out of range" \
                % placement
                )

    def checkFinalPlacement(self, finalPlacements, finalStanding, placementsCount):
        if finalStanding:
            self.checkFinalPlacementRange(finalStanding, placementsCount)
            try:
                finalPlacements.remove(finalStanding)
            except ValueError:
                raise ValueError(
                    "Final statement %s is contained more than once" \
                    % finalStanding
                    )


    def checkTournamentTree(self, matches, groups, teams):
        placementsCount = len(teams)
        finalPlacements = list([x for x in range(1, placementsCount + 1)])

        for match in matches:
            matchId = match['ide']

            winnerFinalStanding  = match.get('winnerFinalStanding')
            looserFinalStanding  = match.get('looserFinalStanding')
            
            self.checkFinalPlacement(
                finalPlacements, winnerFinalStanding, placementsCount
                )

            self.checkFinalPlacement(
                finalPlacements, looserFinalStanding, placementsCount
                )

            # check deadlock
            if winnerFinalStanding == matchId or looserFinalStanding == matchId:
                raise ValueError("Match %s has infinite loop for next process" % matchId)

        for group in groups:
            for advancement in group['advancements']:
                finalPlacement = advancement.get('finalStanding')
                if finalPlacement is not None:
                    self.checkFinalPlacementRange(finalPlacement, placementsCount)
                    finalPlacements.remove(finalPlacement)

        # final check, if all final statements are used
        if len(finalPlacements) != 0:
            raise ValueError("Final placements %s are not reachable" % finalPlacements)

        # check, if all games have only two ways inwards
        processes  = []
        for match in matches:
            if match['winnerNextStepIde']:
                processes.append(match['winnerNextStepIde'])
            if match['looserNextStepIde']:
                processes.append(match['looserNextStepIde'])

        for match in matches:
            # TODO: az budu kontrolovat i skupiny, musim je zde vyradit
            matchId = match['ide']
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
    def saveTournament(self, data, groupMatches, user):
        print "--------------"
        print groupMatches
        # Tournament
        tournamentId = m.Tournament.insert(
            caldTournamentId = data.get('caldTournamentId'),
            city             = data.get('city'),
            country          = data.get('country'),
            divisionId       = data['divisionId'],
            name             = data['name'],
            startDate        = data['startDate'],
            endDate          = data['endDate'],
            teams            = len(data['teams']),
            userId           = user.id
            ).execute()

        # Field
        for field in data['fields']:
            m.Field.insert(tournament = tournamentId, **field).execute()

        # TeamAtTournament
        for team in data['teams']:
            m.TeamAtTournament.insert(
                teamId       = team['id'],
                seeding      = team['seeding'],
                tournamentId = tournamentId
                ).execute()

        # Groups
        # TODO: ulozit skupiny a postupy ze skupin

        for match in data['matches']:

            # Identificators
            identificator, created = m.Identificator.get_or_create(
                tournamentId  = tournamentId,
                ide           = match['ide']
                )

            if match not in groupMatches:
                
                winnerNextStepIde = None
                if match['winnerNextStepIde'] is not None:
                    winnerNextStepIde, created = m.Identificator.get_or_create(
                        tournamentId  = tournamentId,
                        ide           = match['winnerNextStepIde']
                        )
                    winnerNextStepIde = winnerNextStepIde.ide

                looserNextStepIde = None
                if match['looserNextStepIde'] is not None:
                    looserNextStepIde, created = m.Identificator.get_or_create(
                        tournamentId  = tournamentId,
                        ide           = match['looserNextStepIde']
                        )
                    looserNextStepIde = looserNextStepIde.ide

                del match['ide']
                del match['winnerNextStepIde']
                del match['looserNextStepIde']

                print match

                print winnerNextStepIde
                # Match
                matchId = m.Match.insert(
                    tournamentId      = tournamentId,
                    ide               = identificator.ide,
                    looserNextStepIde = looserNextStepIde,
                    winnerNextStepIde = winnerNextStepIde,
                    **match
                    ).execute()

            # else:
            #     del match['ide']
            #     matchId = m.Match.insert(
            #         tournamentId = tournamentId,
            #         identificatorId = identificator.id,
            #         **match
            #         ).execute()

            m.Identificator.\
                update(matchId = matchId).\
                where(m.Identificator.ide == identificator.ide).\
                execute()

        # # Organizer has table
        # if data['user'].role == "organizer":
        #     m.OrganizerHasTournament.insert(
        #             userId = data['user'].id,
        #             tournamentId = tournamentId
        #         ).execute()

        return tournamentId

    # method get is used, where value can be null
    def createTournament(self, req, resp, user):
        data = req.context['data']

        data['user'] = user
        # load term and check it
        startDate = self.getTimestamp(data['startDate'])
        endDate   = self.getTimestamp(data['endDate'])
        if startDate.date() > endDate.date():
            raise ValueError("Tournament has incorrect term (from is after to)")
        
        # check, if division exists
        divisionId = data['divisionId']
        m.Division.get(m.Division.id == divisionId)

        # load and check teams
        teams = data.get('teams')
        self.checkTeams(teams, divisionId)

        # load and check fields
        fields = data.get('fields')
        self.checkFields(fields)
        
        # load groups
        groups = data.get('groups')
        self.checkGroups(groups)

        # load and check matches
        matches = data.get('matches')
        # TODO: nutne otestovat
        self.checkSeedings(matches, len(teams))
        groupMatches = self.checkMatches(matches, startDate, endDate, fields, groups)
        self.checkTournamentTree(matches, groups, teams)
 
        # atomic create tournament
        tournamentId = self.saveTournament(data, groupMatches, user)

        # for result body
        createdTurnament = m.Tournament.get(id=tournamentId)

        return createdTurnament
