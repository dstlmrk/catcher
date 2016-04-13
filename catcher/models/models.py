#!/usr/bin/python
# coding=utf-8

import peewee as pw
from iso3166 import countries
from playhouse.fields import ManyToManyField
from playhouse.fields import DeferredThroughModel
from playhouse.shortcuts import model_to_dict, dict_to_model
import connection

db = connection.connectDatabase()

# -------------------------------------------------------------------------------------
class CountryCode(pw.FixedCharField):
    def db_value(self, value):
        '''Check if field is country by ISO 3166-1 alpha-3'''
        try:
            countries.get(value)
        except KeyError as ex:
            raise KeyError('Country by ISO 3166-1 alpha-3 not found')
        else:
            return value
# -------------------------------------------------------------------------------------
class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""

    def __str__(self):
        return str(model_to_dict(self))

    class Meta:
        database = db
# -------------------------------------------------------------------------------------
class Division(MySQLModel):
    division = pw.CharField()
# -------------------------------------------------------------------------------------
class User(MySQLModel):
    email       = pw.CharField()
    password    = pw.CharField()
    createdAt   = pw.DateTimeField(db_column='created_at')
    lastLoginAt = pw.DateTimeField(db_column='last_login_at')
    nickname    = pw.CharField()

    def prepared(self):
        self.password = None
# -------------------------------------------------------------------------------------
class Club(MySQLModel):
    # id       = pw.PrimaryKeyField()
    user     = pw.IntegerField(db_column='user_id')
    caldId   = pw.IntegerField(db_column='cald_id')
    name     = pw.CharField()
    shortcut = pw.FixedCharField(max_length=3)
    city     = pw.CharField()
    country  = CountryCode(max_length=3)
# -------------------------------------------------------------------------------------
# Placeholder for the through model 
# DeferredClubHasPlayer = DeferredThroughModel()
# -------------------------------------------------------------------------------------
class Player(MySQLModel):
    firstname = pw.CharField()
    lastname  = pw.CharField()
    nickname  = pw.CharField()
    number    = pw.IntegerField()
    ranking   = pw.FloatField()
    caldId    = pw.IntegerField(db_column='cald_id')
    clubId    = pw.IntegerField(db_column='club_id')
    # clubs     = ManyToManyField(Club, through_model=DeferredClubHasPlayer)
# -------------------------------------------------------------------------------------
# class ClubHasPlayer(MySQLModel):
#     club         = pw.ForeignKeyField(Club)
#     player       = pw.ForeignKeyField(Player)
#     caldRelation = pw.BooleanField(db_column='cald_relation')

#     class Meta:
#         primary_key = pw.CompositeKey('club', 'player') 
#         db_table = 'club_has_player'
#         indexes = (
#             (('cald_relation', 'player'), True),
#         )
# -------------------------------------------------------------------------------------
# DeferredClubHasPlayer.set_model(ClubHasPlayer)
# -------------------------------------------------------------------------------------
class Division(MySQLModel):
    id = pw.PrimaryKeyField()
    division = pw.CharField()
# -------------------------------------------------------------------------------------
class Team(MySQLModel):
    clubId     = pw.IntegerField(db_column='club_id')
    divisionId = pw.IntegerField(db_column='division_id')
    degree     = pw.FixedCharField(max_length=1)
    # # TODO: invent, how to remove dependency with db column
    # name       = pw.CharField(db_column='degree')

    # def prepared(self):
    #     self.name = self.club.name + " " + self.degree
# -------------------------------------------------------------------------------------
class CaldTournament(MySQLModel):
    id    = pw.PrimaryKeyField()
    name  = pw.CharField()
    place = pw.CharField()
    date  = pw.DateTimeField()

    class Meta:
        db_table = 'cald_tournament'
# -------------------------------------------------------------------------------------
class Tournament(MySQLModel):
    caldTournamentId = pw.IntegerField(db_column='cald_tournament_id')
    city             = pw.CharField()
    country          = CountryCode()
    divisionId       = pw.IntegerField(db_column='division_id')
    name             = pw.CharField()
    startDate        = pw.DateTimeField(db_column='start_date')
    endDate          = pw.DateTimeField(db_column='end_date')
    teams            = pw.IntegerField()
    ready            = pw.BooleanField()
    terminated       = pw.BooleanField()
# -------------------------------------------------------------------------------------
class Field(MySQLModel):
    id         = pw.IntegerField()
    name       = pw.CharField()
    tournament = pw.ForeignKeyField(Tournament)

    class Meta:
        indexes = (
            (('id', 'tournament'), True),
            (('name', 'tournament'), True),
        )
        # Nemuzu pouzivat, protoze bych jinak nemohl vytvaret nove zaznamy
        # primary_key = pw.CompositeKey('id', 'tournament')
# -------------------------------------------------------------------------------------
class TeamAtTournament(MySQLModel):
    seeding      = pw.IntegerField()
    teamId       = pw.IntegerField(db_column='team_id')
    tournamentId = pw.IntegerField(db_column='tournament_id')

    class Meta:
        db_table = 'team_at_tournament'
        primary_key = False
        # indexes = (
        #     (('tournament', 'team'), True),
        # )
        # primary_key = pw.CompositeKey('team', 'tournament')

    # def prepared(self):
        # self.json = {
        #     "teamId"    : self.team_id,
        #     "name"      : (self.team.club.name + " " + self.team.degree),
        #     "degree"    : self.team.degree,
        #     "divisionId": self.team.division_id,
        #     "seeding"   : self.seeding,
        #     "clubId"    : self.team.club_id
        #     }

# ------------------------------------------------------------------------------------- 
class Identificator(MySQLModel):
    identificator = pw.CharField(max_length=3)
    tournamentId  = pw.IntegerField(db_column='tournament_id')
    matchId       = pw.IntegerField(db_column='match_id')

    class Meta:
        indexes = (
            (('tournament', 'identificator'), True),
        )
        # Nemuzu pouzivat, protoze bych jinak nemohl vytvaret nove zaznamy
        # primary_key = pw.CompositeKey('id', 'tournament')
# ------------------------------------------------------------------------------------- 
class Match(MySQLModel):
    fieldId             = pw.IntegerField(db_column='field_id')
    description         = pw.CharField()
    startTime           = pw.DateTimeField(db_column = 'start_time')
    endTime             = pw.DateTimeField(db_column = 'end_time')
    tournamentId        = pw.IntegerField(db_column='tournament_id')
    terminated          = pw.BooleanField()
    looserFinalStanding = pw.IntegerField(db_column = 'looser_final_standing')
    winnerFinalStanding = pw.IntegerField(db_column = 'winner_final_standing')
    identificatorId     = pw.IntegerField(db_column='identificator_id')
    looserNextStepId    = pw.IntegerField(db_column='looser_next_step')
    winnerNextStepId    = pw.IntegerField(db_column='winner_next_step')
    homeSeed            = pw.IntegerField(db_column = 'home_seed')
    awaySeed            = pw.IntegerField(db_column = 'away_seed')
    flip                = pw.BooleanField()
    awayScore           = pw.IntegerField(db_column = 'away_score')
    homeScore           = pw.IntegerField(db_column = 'home_score')
    spiritAway          = pw.IntegerField(db_column = 'spirit_away')
    spiritHome          = pw.IntegerField(db_column = 'spirit_home')
    awayTeamId          = pw.IntegerField(db_column='away_team_id')
    homeTeamId          = pw.IntegerField(db_column='home_team_id')
    active              = pw.BooleanField()
# -------------------------------------------------------------------------------------
class Standing(MySQLModel):
    standing     = pw.IntegerField()
    teamId       = pw.IntegerField(db_column = 'team_id')
    tournamentId = pw.IntegerField(db_column = 'tournament_id')
    json         = None

    class Meta:
        # pass
        # indexes = (
        #     (('tournament', 'team', 'standing'), True),
        # )
        primary_key = False
        # pw.CompositeKey('standing', 'team', 'tournament')

    def prepared(self):
        self.json = {
            "standing": self.standing,
            "teamId"  : self.teamId
        }
# -------------------------------------------------------------------------------------
class PlayerAtTournament(MySQLModel):
    assists      = pw.IntegerField(default=0)
    matches      = pw.IntegerField(default=0)
    scores       = pw.IntegerField(default=0)
    total        = pw.IntegerField(default=0)
    playerId     = pw.IntegerField(db_column='player_id')
    teamId       = pw.IntegerField(db_column='team_id')
    tournamentId = pw.IntegerField(db_column='tournament_id')
    json         = None

    class Meta:
        db_table = 'player_at_tournament'
        primary_key = False
    #     primary_key = pw.CompositeKey('playerId', 'teamId', 'tournamentId')

    # def prepared(self):
    #     self.json = {
    #         "assists"     : self.assists,
    #         "matches"     : self.matches,
    #         "scores"      : self.scores,
    #         "total"       : self.total,
    #         "playerId"    : self.playerId,
    #         "teamId"      : self.teamId, 
    #         "tournamentId": self.tournamentId
    #         }
# -------------------------------------------------------------------------------------
class PlayerAtMatch(MySQLModel):
    assists    = pw.IntegerField()
    matchId    = pw.IntegerField(db_column='match_id')
    playerId   = pw.IntegerField(db_column='player_id')
    scores     = pw.IntegerField()
    total      = pw.IntegerField()
    
    class Meta:
        primary_key = False
        db_table = 'player_at_match'
# -------------------------------------------------------------------------------------
class Point(MySQLModel):
    homePoint      = pw.BooleanField(db_column='home_point')
    matchId        = pw.IntegerField(db_column='match_id')
    order          = pw.IntegerField()
    assistPlayerId = pw.IntegerField(db_column='assist_player_id')
    scorePlayerId  = pw.IntegerField(db_column='score_player_id')
    awayScore      = pw.IntegerField(db_column='away_score')
    homeScore      = pw.IntegerField(db_column='home_score')
    callahan       = pw.BooleanField()

    class Meta:
        primary_key = False