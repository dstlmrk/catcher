#!/usr/bin/python
# coding=utf-8

from api.resource import Collection, Item
import models as m
from tournamentCreater import TournamentCreater
import falcon
import logging

class TournamentQueries(object):

    @staticmethod
    def getMatchesFromDb(tournamentId, matchId = None):
        findMatch = "" if matchId is None else ("AND match.id = %s" % matchId) 
        q = ("SELECT match.id, identificator.identificator, field.id, field.name," +
             " home_team_id, home_club.name, home_team.degree, away_team_id, away_club.name," +
             " away_team.degree, match.start_time, match.end_time, match.terminated," +
             " match.score_home, match.score_away, match.spirit_home, match.spirit_away," +
             " match.description, match.looser_final_standing, match.winner_final_standing," +
             " winner_next_step.identificator, winner_next_step.match_id, winner_next_step.group_id," +
             " looser_next_step.identificator, looser_next_step.match_id, looser_next_step.group_id," +
             " match.home_seed, match.away_seed FROM catcher.match" +
             " JOIN identificator ON catcher.match.identificator_id = identificator.id" +
             " JOIN field ON field.id = match.field_id AND field.tournament_id = match.tournament_id" +
             " LEFT OUTER JOIN team AS home_team ON home_team.id = match.home_team_id" +
             " LEFT OUTER JOIN team AS away_team ON away_team.id = match.away_team_id" +
             " LEFT OUTER JOIN club AS home_club ON home_club.id = home_team.id" +
             " LEFT OUTER JOIN club AS away_club ON away_club.id = away_team.id" +
             " LEFT OUTER JOIN identificator AS winner_next_step ON winner_next_step.id = match.winner_next_step" +
             " LEFT OUTER JOIN identificator AS looser_next_step ON looser_next_step.id = match.looser_next_step" +
             " WHERE match.tournament_id = %s %s;" % (tournamentId, findMatch))
        qr = m.db.execute_sql(q)
        return qr

    @staticmethod
    def getPlayersFromDb(tournamentId, teamId = None):
        findTeam = "" if teamId is None else ("AND team.id = %s" % teamId) 
        q = ("SELECT team.degree, club.name, team.id, assists, scores, total, matches," +
             " firstname, lastname, nickname, number, player_id" +
             " FROM team_at_tournament INNER JOIN player_at_tournament" + 
             " ON player_at_tournament.team_id = team_at_tournament.team_id" +
             " AND player_at_tournament.tournament_id = team_at_tournament.tournament_id" +
             " INNER JOIN player ON player.id = player_at_tournament.player_id" +
             " INNER JOIN team ON team.id = team_at_tournament.team_id INNER JOIN club" +
             " ON team.club_id = club.id WHERE team_at_tournament.tournament_id = %s %s" 
             % (tournamentId, findTeam) +
             " ORDER BY team.id, total, scores, assists;")
        qr = m.db.execute_sql(q)
        return qr

    @staticmethod
    def getMatches(tournamentId, matchId = None):
        m.Tournament.get(id=tournamentId).id
        qr = TournamentQueries.getMatchesFromDb(tournamentId, matchId)
        matches = []
        for row in qr:
            looserNextStep = None
            if row[20] is not None:
                looserNextStep = {
                    'identificator':row[20],
                    'match_id':row[21],
                    'group_id':row[22]
                }
            winnerNextStep = None
            if row[23] is not None:
                winnerNextStep = {
                    'identificator':row[23],
                    'match_id'     :row[24],
                    'group_id'     :row[25]
                }
            matches.append({
                'id'            : row[0],
                'identificator' : row[1],
                'field'         : {
                    'id'        : row[2],
                    'name'      : row[3]
                    },
                'homeTeam'      : {
                    'id'        : row[4] if row[4] is not None else None,
                    'name'      : (row[5] + " " + row[6]) if row[5] is not None else None,
                    'score'     : row[13],
                    'spirit'    : row[15],
                    'seed'      : row[26]
                    },
                'awayTeam'      : {
                    'id'        : row[7] if row[4] is not None else None,
                    'name'      : (row[8] + " " + row[9]) if row[5] is not None else None,
                    'score'     : row[14],
                    'spirit'    : row[16],
                    'seed'      : row[27]
                    },
                'time'          : {
                    'start'     : row[10],
                    'end'       : row[11]
                    },
                'terminated'    : row[12],
                'description'   : row[17],
                'looser'        : {
                    'finalStanding': row[18],
                    'nextStep'  : looserNextStep
                    },
                'winner'        : {
                    'finalStanding': row[19],
                    'nextStep'  : winnerNextStep
                    }
                })

        result = {
            'count'  : len(matches), 
            'matches': matches
        }
        return result

    @staticmethod
    def getPlayersPerTeams(tournamentId, teamId = None):
        m.Tournament.get(id = tournamentId).id
        qr = TournamentQueries.getPlayersFromDb(tournamentId, teamId)
        teams = list()
        for row in qr:
            teamName = (row[1] + " " + row[0])
            teamId = row[2]
            teams.append({'name':teamName, 'id':teamId, 'players':[]})
        # temporary dict with the key being the id
        teams = {v['id']:v for v in teams}
        for row in qr:
            teamId    = row[2]
            teams[teamId]['players'].append({
                'assists'  : row[3],
                'scores'   : row[4],
                'total'    : row[5],
                'matches'  : row[6],
                'firstname': row[7],
                'lastname' : row[8],
                'nickname' : row[9],
                'number'   : row[10],
                'id'       : row[11]
                })
        result = {
            'count': len(teams),
            'teams': teams.values()
        }
        return result

    @staticmethod
    def getPlayersPerTournament(tournamentId):
        qr = TournamentQueries.getPlayersFromDb(tournamentId, None)
        players = list()
        for row in qr:
            teamId    = row[2]
            players.append({
                'assists'  : row[3],
                'scores'   : row[4],
                'total'    : row[5],
                'matches'  : row[6],
                'firstname': row[7],
                'lastname' : row[8],
                'nickname' : row[9],
                'number'   : row[10],
                'id'       : row[11]
                })
        result = {
            'count'  : len(players),
            'players': players
        }
        return result

class Tournament(Item):

    @m.db.atomic()
    def activeTournament(self, id):
        tournament = m.Tournament.\
            select(m.Tournament.teams, m.Tournament.active).\
            where(m.Tournament.id == id).get()

        if tournament.active:
            raise ValueError("Tournament %s is already active" % id)

        teams = m.TeamAtTournament.select().\
            where(m.TeamAtTournament.tournament == id).dicts()

        if len(teams) != tournament.teams:
            raise Exception(
                "Tournament has different number of teams"
                " in contrast to TeamAtTournament" % matchId
                )

        # active Tournament
        m.Tournament.update(active=True).where(m.Tournament.id==id).execute()

        # Standing
        for x in range(1, len(teams)+1):
             m.Standing.insert(
                tournament = id,
                standing = x
                ).execute()

        # Matches
        teamsAdSeeding = {}
        for team in teams:
            teamsAdSeeding[team['seeding']] = team['team']

        matches = m.Match.select().\
            where(
                m.Match.tournament == 1 and \
                (m.Match.homeSeed != None or m.Match.awaySeed != None) 
                )

        for match in matches:
            m.Match.update(
                homeTeam = teamsAdSeeding[match.homeSeed],
                awayTeam = teamsAdSeeding[match.awaySeed]
                ).\
                where(m.Match.id == match.id).execute()

    @m.db.atomic()    
    def terminateTournament(self, id):
        logging.warning("Tournament.terminateTournament() neni implementovano")

    def on_put(self, req, resp, id):
        requestBody = req.context['data']

        tournament = m.Tournament.select(m.Tournament).where(m.Tournament.id==id).get()

        if tournament.active is False and requestBody.get('active') is True:
            self.activeTournament(id)

        if tournament.terminated is False and requestBody.get('terminated') is True:
            self.terminateTournament(id)

        super(Tournament, self).on_put(req, resp, id,
            ['name', 'startDate', 'endDate', 'city', 'country', 'caldTournametId']
            )


class Tournaments(Collection):
    
    def on_post(self, req, resp):
        tournamentCreater = TournamentCreater()
        createdTurnament = tournamentCreater.createTournament(req, resp)
        req.context['result'] = createdTurnament 
        resp.status = falcon.HTTP_201


class TournamentStandings(object):

    def on_get(self, req, resp, id):
        tournament = m.Tournament.select(m.Tournament.active, m.Tournament.terminated).where(m.Tournament.id==id).get()
        if not tournament.active and not tournament.terminated:
            raise ValueError("Tournament hasn't any standings")

        qr = m.Standing.select().where(m.Standing.tournament==id)
        items = []
        for standing in qr:
            items.append({
                "standing": standing.standing,
                "team": standing.team if standing.team_id else None
                })
        collection = {
            'count' : len(items),
            'items' : items
        }
        req.context['result'] = collection

class TournamentTeams(object):

    def on_get(self, req, resp, id):
        teams = m.TeamAtTournament.\
            select(m.TeamAtTournament.team).\
            where(m.TeamAtTournament.tournament==id)
        items = []
        for team in teams:
            items.append(team.team)
        collection = {
            'count' : len(items),
            'items' : items
        }
        req.context['result'] = collection

class TournamentMatches(object):

    def on_get(self, req, resp, id):
        req.context['result'] = TournamentQueries.getMatches(
            tournamentId = id
            )

class TournamentMatch(object):

    def on_get(self, req, resp, id, matchId):
        req.context['result'] = TournamentQueries.getMatches(
            tournamentId = id,
            matchId = matchId
            )

class TournamentTeamsAndPlayers(object):

    def on_get(self, req, resp, id):
        req.context['result'] = TournamentQueries.getPlayersPerTeams(
            tournamentId = id
            )

class TournamentTeamAndPlayers(object):

    def on_get(self, req, resp, id, teamId):
        req.context['result'] = TournamentQueries.getPlayersPerTeams(
            tournamentId = id,
            teamId = teamId
            )

class TournamentPlayers(object):

    # TODO: jako parametr zde muze byt limit
    def on_get(self, req, resp, id):
        req.context['result'] = TournamentQueries.getPlayersPerTournament(
            tournamentId = id
            )
