#!/usr/bin/python
# coding=utf-8
from iso3166 import countries

import peewee as pw
# import MySQLdb

db = pw.MySQLDatabase('catcher', user='', passwd='', host='localhost')

DBNAME     = 'catcher'
TABLE_CLUB = 'club'
TABLE_USER = 'user'

class CountryCode(pw.FixedCharField):
    def db_value(self, value):
        '''Check if field is country by ISO 3166-1 alpha-3'''
        try:
            countries.get(value)
        except KeyError as ex:
            raise KeyError("Country by ISO 3166-1 alpha-3 not found")
        else:
            return value

class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db

class User(MySQLModel):
    email    = pw.CharField()
    password = pw.CharField()
    # etc, etc

class Club(MySQLModel):
    id       = pw.PrimaryKeyField()
    user_id  = pw.ForeignKeyField(User)
    cald_id  = pw.IntegerField()
    name     = pw.CharField()
    shortcut = pw.FixedCharField(max_length=3)
    city     = pw.CharField()
    country  = pw.FixedCharField(max_length=3)

# when you're ready to start querying, remember to connect
db.connect()

# db.create_tables([User])


# id, user_id, cald_id, name, shortcut, city, country

# charlie = Club.create(email='charlie', password='xx')

# huey = User(username='huey')
# huey.save()
