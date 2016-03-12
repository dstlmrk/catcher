#!/usr/bin/python
# coding=utf-8

import peewee as pw
from iso3166 import countries

# from peewee import playhouse.fields.ManyToManyField

from playhouse.fields import ManyToManyField

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
    class Meta:
        database = db

class User(MySQLModel):
    email    = pw.CharField()
    password = pw.CharField()

# Create a reference object to stand in for our as-yet-undefined Tweet model.
DeferredClub   = pw.DeferredRelation()
DeferredPlayer = pw.DeferredRelation()
DeferredClubHasPlayer = pw.DeferredRelation()

class ClubHasPlayer(MySQLModel):
    club   = pw.ForeignKeyField(DeferredClub)
    player = pw.ForeignKeyField(DeferredPlayer)

    class Meta:
        primary_key = pw.CompositeKey('club', 'player')
        db_table = 'club_has_player'
        # primary_key = False

class Club(MySQLModel):
    id       = pw.PrimaryKeyField()
    # kdyz jde o klic, nemusi mit sufix '_id'
    user     = pw.ForeignKeyField(User)
    cald_id  = pw.IntegerField()
    name     = pw.CharField()
    shortcut = pw.FixedCharField(max_length=3)
    city     = pw.CharField()
    country  = CountryCode(max_length=3)

    players  = ManyToManyField(DeferredPlayer, through_model=ClubHasPlayer)

DeferredClub.set_model(Club)

class Player(MySQLModel):
    id        = pw.PrimaryKeyField()
    firstname = pw.CharField()
    lastname  = pw.CharField()
    nickname  = pw.CharField()
    number    = pw.IntegerField()
    cald_id   = pw.IntegerField()
    ranking   = pw.FloatField()

    clubs  = ManyToManyField(Club, through_model=ClubHasPlayer)

DeferredPlayer.set_model(Player)


# when you're ready to start querying, remember to connect
db.connect()

# Now that Tweet is defined, we can initialize the reference.
# DeferredClub.set_model(Club)
# DeferredPlayer.set_model(Player)