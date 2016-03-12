#!/usr/bin/python
# coding=utf-8

import peewee as pw
from iso3166 import countries

# from peewee import playhouse.fields.ManyToManyField

from playhouse.fields import ManyToManyField
from playhouse.fields import DeferredThroughModel
# from playhouse.

# TODO: udaje nacitat z configu
db = pw.MySQLDatabase('catcher', user='', passwd='', host='localhost')

# TODO: tabulky nacitat z configu
DBNAME                = 'catcher'
TABLE_CLUB            = 'club'
TABLE_PLAYER          = 'player'
TABLE_USER            = 'user'
TABLE_CLUB_HAS_PLAYER = 'club_has_player'

class CountryCode(pw.FixedCharField):
    def db_value(self, value):
        '''Check if field is country by ISO 3166-1 alpha-3'''
        try:
            countries.get(value)
        except KeyError as ex:
            raise KeyError('Country by ISO 3166-1 alpha-3 not found')
        else:
            return value

class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""

    def __str__(self):
        # TODO: replace this private variable
        return str(self._data)

    class Meta:
        database = db

class User(MySQLModel):
    email    = pw.CharField()
    password = pw.CharField()

class Player(MySQLModel):
    # id        = pw.PrimaryKeyField()
    firstname    = pw.CharField()
    lastname     = pw.CharField()
    nickname     = pw.CharField()
    number       = pw.IntegerField()
    ranking      = pw.FloatField()
    cald_id      = pw.IntegerField()
    cald_club_id = pw.IntegerField()

# Placeholder for the through model 
DeferredClubHasPlayer = DeferredThroughModel()

class Club(MySQLModel):
    # id       = pw.PrimaryKeyField()
    user     = pw.ForeignKeyField(User)
    cald_id  = pw.IntegerField()
    name     = pw.CharField()
    shortcut = pw.FixedCharField(max_length=3)
    city     = pw.CharField()
    country  = CountryCode(max_length=3)
    players  = ManyToManyField(Player, through_model=DeferredClubHasPlayer)

class ClubHasPlayer(MySQLModel):
    club   = pw.ForeignKeyField(Club)
    player = pw.ForeignKeyField(Player)

    class Meta:
        primary_key = pw.CompositeKey('club', 'player')
        db_table = 'club_has_player'
        # primary_key = False

DeferredClubHasPlayer.set_model(ClubHasPlayer)

# when you're ready to start querying, remember to connect
db.connect()