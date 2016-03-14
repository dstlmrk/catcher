#!/usr/bin/python
# coding=utf-8

import peewee as pw
from iso3166 import countries
from playhouse.fields import ManyToManyField
from playhouse.fields import DeferredThroughModel
from playhouse.shortcuts import model_to_dict

# Print all queries to stderr.
import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# TODO: udaje nacitat z configu
db = pw.MySQLDatabase('catcher', user='', passwd='', host='localhost')

# -------------------------------------------------------------------
class CountryCode(pw.FixedCharField):
    def db_value(self, value):
        '''Check if field is country by ISO 3166-1 alpha-3'''
        try:
            countries.get(value)
        except KeyError as ex:
            raise KeyError('Country by ISO 3166-1 alpha-3 not found')
        else:
            return value
# -------------------------------------------------------------------
class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""

    def __str__(self):
        # TODO: replace this private method
        # return str(self._data)
        return str(model_to_dict(self))
        # return str(model_to_dict(self._data))

    class Meta:
        database = db
# -------------------------------------------------------------------
class User(MySQLModel):
    email    = pw.CharField()
    password = pw.CharField()
# -------------------------------------------------------------------
class Club(MySQLModel):
    # id       = pw.PrimaryKeyField()
    user     = pw.ForeignKeyField(User)
    caldId   = pw.IntegerField(db_column='cald_id')
    name     = pw.CharField()
    shortcut = pw.FixedCharField(max_length=3)
    city     = pw.CharField()
    country  = CountryCode(max_length=3)
# -------------------------------------------------------------------
# Placeholder for the through model 
DeferredClubHasPlayer = DeferredThroughModel()
# -------------------------------------------------------------------
class Player(MySQLModel):
    firstname = pw.CharField()
    lastname  = pw.CharField()
    nickname  = pw.CharField()
    number    = pw.IntegerField()
    ranking   = pw.FloatField()
    caldId    = pw.IntegerField(db_column='cald_id')
    # club      = pw.ForeignKeyField(Club, related_name='received_messages')
    clubs     = ManyToManyField(Club, through_model=DeferredClubHasPlayer)
# -------------------------------------------------------------------
class ClubHasPlayer(MySQLModel):
    club         = pw.ForeignKeyField(Club)
    player       = pw.ForeignKeyField(Player)
    caldRelation = pw.BooleanField(db_column='cald_relation')

    class Meta:
        primary_key = pw.CompositeKey('club', 'player') 
        db_table = 'club_has_player'
        # primary_key = False
# -------------------------------------------------------------------
DeferredClubHasPlayer.set_model(ClubHasPlayer)
# -------------------------------------------------------------------
class Division(MySQLModel):
    division = pw.CharField()
# -------------------------------------------------------------------
class Team(MySQLModel):
    # related_name='teams'
    club       = pw.ForeignKeyField(Club, db_column='club_id', related_name='teams')
    # related_name='divison'
    division   = pw.ForeignKeyField(Division, db_column='division_id')
    degree     = pw.FixedCharField(max_length=1)
# -------------------------------------------------------------------
# TODO: only for deployment, in every single script I must added it
# when you're ready to start querying, remember to connect
db.connect()