#!/usr/bin/python
# coding=utf-8

import peewee as pw
from iso3166 import countries
from playhouse.fields import ManyToManyField
from playhouse.fields import DeferredThroughModel
from playhouse.shortcuts import model_to_dict, dict_to_model
import config

db = pw.MySQLDatabase(
    config.db.login['db'],
    user   = config.db.login['user'],
    passwd = config.db.login['passwd'],
    host   = config.db.login['host']
    )

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
    #     # TODO: replace this private method
        # return str(self._data)
        return str(model_to_dict(self))
        # return str(model_to_dict(self._data))

    class Meta:
        database = db
# -------------------------------------------------------------------------------------
class User(MySQLModel):
    email    = pw.CharField()
    password = pw.CharField()
# -------------------------------------------------------------------------------------
class Club(MySQLModel):
    # id       = pw.PrimaryKeyField()
    user     = pw.ForeignKeyField(User)
    caldId   = pw.IntegerField(db_column='cald_id')
    name     = pw.CharField()
    shortcut = pw.FixedCharField(max_length=3)
    city     = pw.CharField()
    country  = CountryCode(max_length=3)
# -------------------------------------------------------------------------------------
# Placeholder for the through model 
DeferredClubHasPlayer = DeferredThroughModel()
# -------------------------------------------------------------------------------------
class Player(MySQLModel):
    firstname = pw.CharField()
    lastname  = pw.CharField()
    nickname  = pw.CharField()
    number    = pw.IntegerField()
    ranking   = pw.FloatField()
    caldId    = pw.IntegerField(db_column='cald_id')
    # club      = pw.ForeignKeyField(Club, related_name='received_messages')
    clubs     = ManyToManyField(Club, through_model=DeferredClubHasPlayer)
# -------------------------------------------------------------------------------------
class ClubHasPlayer(MySQLModel):
    club         = pw.ForeignKeyField(Club)
    player       = pw.ForeignKeyField(Player)
    caldRelation = pw.BooleanField(db_column='cald_relation')

    class Meta:
        primary_key = pw.CompositeKey('club', 'player') 
        db_table = 'club_has_player'
        indexes = (
            (('cald_relation', 'player'), True),
        )
# -------------------------------------------------------------------------------------
DeferredClubHasPlayer.set_model(ClubHasPlayer)
# -------------------------------------------------------------------------------------
class Division(MySQLModel):
    division = pw.CharField()
# -------------------------------------------------------------------------------------
class Team(MySQLModel):
    club       = pw.ForeignKeyField(Club, db_column='club_id', related_name='teams')
    division   = pw.ForeignKeyField(Division, db_column='division_id')
    degree     = pw.FixedCharField(max_length=1)
    # TODO: invent, how to remove dependency with db column
    name       = pw.CharField(db_column='degree')

    def prepared(self):
        self.name = self.club.name + " " + self.degree
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
    caldTournament   = pw.ForeignKeyField(CaldTournament, db_column='cald_tournament_id')
    city             = pw.CharField()
    country          = CountryCode()
    division         = pw.ForeignKeyField(Division, db_column='division_id')
    name             = pw.CharField()
    startDate        = pw.DateTimeField(db_column='start_date')
    endDate          = pw.DateTimeField(db_column='end_date')
    teams            = pw.IntegerField()
    active           = pw.BooleanField()
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
    seeding    = pw.IntegerField()
    team       = pw.ForeignKeyField(Team)
    tournament = pw.ForeignKeyField(Tournament)

    class Meta:
        db_table = 'team_at_tournament'
        indexes = (
            (('tournament', 'team'), True),
        )
        primary_key = pw.CompositeKey('team', 'tournament')

    # TODO: MAGICKE METODY
    # TODO: zkusit se podivat, jak by se daly ziskavat jednotlive objekty a jake data k nim
    # def __getitem__(self, obj):
        # return "XXX"
# ------------------------------------------------------------------------------------- 
class Identificator(MySQLModel):
    identificator = pw.CharField(max_length=3)
    tournament    = pw.ForeignKeyField(Tournament)
    matchId       = pw.IntegerField(db_column='match_id')

    class Meta:
        indexes = (
            (('tournament', 'identificator'), True),
        )
        # Nemuzu pouzivat, protoze bych jinak nemohl vytvaret nove zaznamy
        # primary_key = pw.CompositeKey('id', 'tournament')
# ------------------------------------------------------------------------------------- 
class Match(MySQLModel):
    field               = pw.ForeignKeyField(Field)
    description         = pw.CharField()
    startTime           = pw.DateTimeField(db_column = 'start_time')
    endTime             = pw.DateTimeField(db_column = 'end_time')
    tournament          = pw.ForeignKeyField(Tournament)
    terminated          = pw.BooleanField()
    looserFinalStanding = pw.IntegerField(db_column = 'looser_final_standing')
    winnerFinalStanding = pw.IntegerField(db_column = 'winner_final_standing')
    identificator       = pw.ForeignKeyField(Identificator)
    looserNextStep      = pw.ForeignKeyField(rel_model = Identificator,
                                             db_column = 'looser_next_step',
                                             related_name = 'looserIds') 
    winnerNextStep      = pw.ForeignKeyField(rel_model = Identificator,
                                             db_column = 'winner_next_step',
                                             related_name = 'winnerIds')
    # TODO: musi existovat akce, kde odstartuje turnaj a doplni tymy
    homeSeed            = pw.IntegerField(db_column = 'home_seed')
    awaySeed            = pw.IntegerField(db_column = 'away_seed')

    flip                = pw.BooleanField()
    scoreAway           = pw.IntegerField(db_column = 'score_away')
    scoreHome           = pw.IntegerField(db_column = 'score_home')
    spiritAway          = pw.IntegerField(db_column = 'spirit_away')
    spiritHome          = pw.IntegerField(db_column = 'spirit_home')
    awayTeam            = pw.ForeignKeyField(rel_model    = Team,
                                             db_column    = 'away_team_id',
                                             related_name = 'matchesAsHome')
    homeTeam            = pw.ForeignKeyField(rel_model    = Team,
                                             db_column    = 'home_team_id',
                                             related_name = 'matchesAsAway')
# -------------------------------------------------------------------------------------
class Standing(MySQLModel):
    standing   = pw.IntegerField()
    team       = pw.ForeignKeyField(Team)
    tournament = pw.ForeignKeyField(Tournament)

    class Meta:
        indexes = (
            (('tournament', 'team', 'standing'), True),
        )
        primary_key = pw.CompositeKey('standing', 'team', 'tournament')
# -------------------------------------------------------------------------------------
class PlayerAtTournament(MySQLModel):
    assists    = pw.IntegerField(default=0)
    matches    = pw.IntegerField(default=0)
    scores     = pw.IntegerField(default=0)
    total      = pw.IntegerField(default=0)
    player     = pw.ForeignKeyField(Player)
    team       = pw.ForeignKeyField(Team)
    tournament = pw.ForeignKeyField(Tournament)

    class Meta:
        db_table = 'player_at_tournament'
        primary_key = False
        # primary_key = CompositeKey('player', 'team', 'tournament')
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------