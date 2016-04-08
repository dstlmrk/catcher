#!/usr/bin/python
# coding=utf-8

from api.resource import Collection, Item
import models as m
from tournamentCreater import TournamentCreater
import falcon
import logging
import datetime

class TournamentQueries(object):

    @staticmethod
    def getMatches(tournamentId, matchId = None, fieldId = None, date = None, active = None, terminated = None):
        whereMatch      = "" if matchId is None else ("AND match.id = %s" % matchId) 
        whereField      = "" if fieldId is None else ("AND field.id = %s" % fieldId) 
        whereDate       = "" if date is None else ("AND DATE(match.start_time) = %s" % date) 
        whereActive     = "" if active is None else ("AND match.active = %s" % active) 
        whereTerminated = "" if terminated is None else ("AND match.terminated = %s" % terminated) 
        q = ("SELECT match.id, identificator.identificator, field.id, field.name,"
             " home_team_id, home_club.name, home_team.degree, away_team_id, away_club.name,"
             " away_team.degree, match.start_time, match.end_time, match.terminated,"
             " match.home_score, match.away_score, match.spirit_home, match.spirit_away,"
             " match.description, match.looser_final_standing, match.winner_final_standing,"
             " winner_next_step.identificator, winner_next_step.match_id, winner_next_step.group_id,"
             " looser_next_step.identificator, looser_next_step.match_id, looser_next_step.group_id,"
             " match.home_seed, match.away_seed, match.active FROM catcher.match"
             " JOIN identificator ON catcher.match.identificator_id = identificator.id"
             " JOIN field ON field.id = match.field_id AND field.tournament_id = match.tournament_id"
             " LEFT OUTER JOIN team AS home_team ON home_team.id = match.home_team_id"
             " LEFT OUTER JOIN team AS away_team ON away_team.id = match.away_team_id"
             " LEFT OUTER JOIN club AS home_club ON home_club.id = home_team.id"
             " LEFT OUTER JOIN club AS away_club ON away_club.id = away_team.id"
             " LEFT OUTER JOIN identificator AS winner_next_step ON winner_next_step.id = match.winner_next_step"
             " LEFT OUTER JOIN identificator AS looser_next_step ON looser_next_step.id = match.looser_next_step"
             " WHERE match.tournament_id = %s %s %s %s %s %s;" 
             % (tournamentId, whereMatch, whereField, whereDate, whereActive, whereTerminated)
             )
        qr = m.db.execute_sql(q)
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
                    },
                'active'        : row[28]
                })
        return matches

    @staticmethod
    def getPlayers(tournamentId, teamId = None, limit = None):
        whereTeam = "" if teamId is None else ("AND team.id = %s" % teamId)
        limit = "" if limit is None else ("LIMIT %s" % limit)
        q = ("SELECT team.degree, club.name, team.id, assists, scores, total, matches,"
             " firstname, lastname, nickname, number, player_id"
             " FROM team_at_tournament INNER JOIN player_at_tournament"
             " ON player_at_tournament.team_id = team_at_tournament.team_id"
             " AND player_at_tournament.tournament_id = team_at_tournament.tournament_id"
             " INNER JOIN player ON player.id = player_at_tournament.player_id"
             " INNER JOIN team ON team.id = team_at_tournament.team_id INNER JOIN club"
             " ON team.club_id = club.id WHERE team_at_tournament.tournament_id = %s %s" 
             " ORDER BY total, scores, assists %s;" % (tournamentId, whereTeam, limit)
             )
        qr = m.db.execute_sql(q)
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
        return players

class Tournament(Item):

    @m.db.atomic()
    def prepareTournament(self, id):
        tournament = m.Tournament.\
            select(m.Tournament.teams, m.Tournament.ready).\
            where(m.Tournament.id == id).get()

        if tournament.ready:
            raise ValueError("Tournament %s is already ready" % id)

        teams = m.TeamAtTournament.select().\
            where(m.TeamAtTournament.tournament == id).dicts()

        if len(teams) != tournament.teams:
            raise Exception(
                "Tournament has different number of teams"
                " in contrast to TeamAtTournament" % matchId
                )

        # ready Tournament
        m.Tournament.update(ready=True).where(m.Tournament.id==id).execute()

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

        super(Tournament, self).on_put(req, resp, id,
            ['active', 'name', 'startDate', 'endDate', 'city', 'country', 'caldTournametId']
            )

        edited = False
        if tournament.ready is False and requestBody.get('ready') is True:
            self.prepareTournament(id)
            edited = True

        if tournament.terminated is False and requestBody.get('terminated') is True:
            self.terminateTournament(id)
            edited = True

        if edited:
            resp.status = falcon.HTTP_200 


class Tournaments(Collection):
    
    def on_post(self, req, resp):
        tournamentCreater = TournamentCreater()
        createdTurnament = tournamentCreater.createTournament(req, resp)
        req.context['result'] = createdTurnament 
        resp.status = falcon.HTTP_201


class TournamentStandings(object):

    def on_get(self, req, resp, id):
        tournament = m.Tournament.select(m.Tournament.ready, m.Tournament.terminated).where(m.Tournament.id==id).get()
        if not tournament.ready and not tournament.terminated:
            raise ValueError("Tournament hasn't any standings")
        qr = m.Standing.select().where(m.Standing.tournament==id)
        standings = []
        for standing in qr:
            standings.append(standing.json)
        collection = {
            'teams'     : len(standings),
            'standings' : standings,
            'spirit'    : "UNFINISHED"
            }
        req.context['result'] = collection

class TournamentTeams(object):

    def on_get(self, req, resp, id):
        teams = m.TeamAtTournament.\
            select(m.TeamAtTournament, m.TeamAtTournament.team).\
            where(m.TeamAtTournament.tournament==id)
        items = []
        for team in teams:
            items.append(team.json)
        collection = {
            'count' : len(items),
            'items' : items
        }
        req.context['result'] = collection

    def on_put(self, req, resp, id):
        prepared =  m.Tournament.select(m.Tournament.ready).where(m.Tournament.id==id).get().ready
        if ready:
            raise ValueError("Tournament is ready and teams can't be changed")
        requestBody = req.context['data']
        qr = m.TeamAtTournament.\
            update(
                team    = requestBody['teamId']
                ).\
            where(
                m.TeamAtTournament.tournament == id,
                m.TeamAtTournament.seeding == requestBody['seeding']
            ).execute()
        resp.status = falcon.HTTP_200 if qr else falcon.HTTP_304
        req.context['result'] =  m.TeamAtTournament.get(
            tournament = id,
            seeding = requestBody['seeding']
            )

class TournamentMatches(object):

    def on_get(self, req, resp, id):
        matches = TournamentQueries.getMatches(
            id,
            req.params.get('matchId'),
            req.params.get('fieldId'),
            req.params.get('date'),
            req.params.get('active'),
            req.params.get('terminated')
            )

        collection = {
            'count'  : len(matches),
            'matches': matches
        }
        
        req.context['result'] = collection

    def on_put(self, req, resp, id):
        editableCols = [
            'active', 'fieldId', 'startTime', 'endTime', 'terminated', 'description'
            ]
        requestBody = req.context['data']
        matchId = requestBody['matchId']
        if editableCols is not None:
            params = { key : requestBody[key] for key in requestBody if key in editableCols}
        qr = None
        if params and matchId:
            qr = m.Match.update(**params).where(
                m.Match.tournament==id and m.Match.id==matchId
                ).execute()
        matches = TournamentQueries.getMatches(id, matchId)
        req.context['result'] = matches
        resp.status = falcon.HTTP_200 if qr else falcon.HTTP_304

class TournamentPlayers(object):

    def on_get(self, req, resp, id):
        players = TournamentQueries.getPlayers(
            id, req.params.get('teamId'), req.params.get('limit')
            )

        collection = {
            'count': len(players),
            'players': players
        }
        
        req.context['result'] = collection

    def on_post(self, req, resp, id):
        teamId   = req.context['data'].get('teamId')
        playerId = req.context['data'].get('playerId')

        r = m.PlayerAtTournament.insert(
            tournament = id,
            team       = teamId,
            player     = playerId
            ).execute()

        newPlayer = m.PlayerAtTournament.get(
            tournament = id,
            team       = teamId,
            player     = playerId
            )

        resp.status = falcon.HTTP_201 if r else falcon.HTTP_200
        req.context['result'] = newPlayer.json

    def on_delete(self, req, resp, id):
        teamId   = req.context['data'].get('teamId')
        playerId = req.context['data'].get('playerId')
        
        matches = m.PlayerAtTournament.get(
            m.PlayerAtTournament.tournament == id,
            m.PlayerAtTournament.team       == teamId,
            m.PlayerAtTournament.player     == playerId
            ).matches

        if matches == 0:
            d = m.PlayerAtTournament.delete().where(
                m.PlayerAtTournament.tournament == id,
                m.PlayerAtTournament.team       == teamId,
                m.PlayerAtTournament.player     == playerId
                ).execute()
        else:
            raise ValueError("Player has played matches")

class TournamentGroups(object):
    pass