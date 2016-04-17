#!/usr/bin/python
# coding=utf-8

from catcher import models as m
from playhouse.shortcuts import model_to_dict

class Queries(object):

    @staticmethod
    def getClubs(clubId = None):
        whereClub = "" if clubId is None else (" WHERE club.id = %s" % clubId)
        q = ("SELECT club.id, club.cald_id, club.name, club.shortcut, club.city, club.country," +
             " user.created_at"
             " FROM club LEFT OUTER JOIN user ON user.id = club.user_id %s"
             % (whereClub))
        qr = m.db.execute_sql(q)
        clubs = []
        for row in qr:
            user = None
            if row[6] is not None:
                user = {'createdAt'   : row[6]}
            clubs.append({
                'id'      : row[0],
                'caldId'  : row[1],
                'name'    : row[2],
                'shortcut': row[3],
                'city'    : row[4],
                'country' : row[5],
                'user'    : user
                })
        return clubs

    @staticmethod
    def getPoints(matchId, order = None):
        '''returns all points from the match'''
        whereOrder = "" if order is None else ("AND point.order = %s" % order) 
        q = ("SELECT match_id, point.order, assist_player_id, score_player_id,"
             " home_score, away_score, home_point, callahan,"
             " ap.firstname, ap.lastname, sp.firstname, sp.lastname"
             " FROM point LEFT OUTER JOIN player AS ap ON ap.id = point.assist_player_id"
             " LEFT OUTER JOIN player AS sp ON sp.id = point.score_player_id"
             " WHERE match_id = %s %s ORDER BY point.order DESC;"
             % (matchId, whereOrder))

        qr = m.db.execute_sql(q)
        points = []
        for row in qr:
            points.append({
                'matchId'      : row[0],       
                'order'        : row[1],
                'assistPlayer' : {
                    'id'       : row[2],
                    'firstname': row[8],
                    'lastname' : row[9]
                },
                'scorePlayer'  : {
                    'id'       : row[3],
                    'firstname': row[10],
                    'lastname' : row[11]
                },
                'homeScore'    : row[4],
                'awayScore'    : row[5],
                'homePoint'    : row[6],
                'callahan'     : row[7]
                })
        return points

    @staticmethod
    def getLastPoint(matchId):
        '''returns tripe'''
        q = ("SELECT point.order, home_score, away_score"
             " FROM point WHERE match_id = %s ORDER BY point.order DESC LIMIT 1;"
             % (matchId)
             )
        qr =  m.db.execute_sql(q).fetchone()
        return qr if qr else (0, 0, 0)

    @staticmethod
    def getMatches(tournamentId = None, matchId = None, fieldId = None, date = None, active = None, terminated = None):
        whereTournament = "" if tournamentId is None else ("AND match.tournament_id = %s" % tournamentId)
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
             " match.home_seed, match.away_seed, match.active FROM `match`"
             " JOIN identificator ON match.identificator_id = identificator.id"
             " JOIN field ON field.id = match.field_id AND field.tournament_id = match.tournament_id"
             " LEFT OUTER JOIN team AS home_team ON home_team.id = match.home_team_id"
             " LEFT OUTER JOIN team AS away_team ON away_team.id = match.away_team_id"
             " LEFT OUTER JOIN club AS home_club ON home_club.id = home_team.id"
             " LEFT OUTER JOIN club AS away_club ON away_club.id = away_team.id"
             " LEFT OUTER JOIN identificator AS winner_next_step ON winner_next_step.id = match.winner_next_step"
             " LEFT OUTER JOIN identificator AS looser_next_step ON looser_next_step.id = match.looser_next_step"
             " WHERE 1 %s %s %s %s %s %s;" 
             % (whereTournament, whereMatch, whereField, whereDate, whereActive, whereTerminated)
             )
        qr = m.db.execute_sql(q)
        matches = []
        for row in qr:
            looserNextStep = None
            if row[20] is not None:
                looserNextStep = {
                    'identificator':row[20],
                    'matchId':row[21],
                    'groupId':row[22]
                }
            winnerNextStep = None
            if row[23] is not None:
                winnerNextStep = {
                    'identificator':row[23],
                    'matchId'     :row[24],
                    'groupId'     :row[25]
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

    @staticmethod
    def getTeams(tournamentId, teamId = None):
        
        whereTeam = "" if teamId is None else ("AND team.id = %s" % teamId)
        q = ("SELECT team.id, degree, club.id, name, division_id, seeding"
             " FROM team_at_tournament" 
             " JOIN team ON team_at_tournament.team_id = team.id" 
             " JOIN club ON team.club_id = club.id"
             " WHERE tournament_id = %s %s;"
             % (tournamentId, whereTeam)
            )
        qr = m.db.execute_sql(q)
        teams = list()
        for row in qr:
            teams.append({
                'teamId'    : row[0],
                'degree'    : row[1],
                'clubId'    : row[2],
                'name'      : (row[3] + " " + row[1]),
                'divisionId': row[4],
                'seeding'   : row[5]
                })
        return teams

    @staticmethod
    def getPlayersTeamId(tournamentId, teamId):
        '''returns one number'''
        q = ("SELECT team_id FROM player_at_tournament"
             " WHERE tournament_id = %s AND player_id = %s;"
             % (tournamentId, teamId)
             )
        return m.db.execute_sql(q).fetchone()[0]
