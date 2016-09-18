#!/usr/bin/python
# coding=utf-8

import peewee as pw
from catcher.models import MySQLModel, CountryCode, Division

SHORTCUT_MAX_LENGTH = 3


class Team(MySQLModel):

    division = pw.ForeignKeyField(Division)
    name = pw.CharField()
    shortcut = pw.CharField(max_length=SHORTCUT_MAX_LENGTH)
    city = pw.CharField()
    country = CountryCode(max_length=3)
    cald_id = pw.IntegerField()
    user_id = pw.IntegerField()

    @classmethod
    def create(cls, *args, **kw):
        '''Creates new user and validates input data'''
        if kw.get('shortcut'):
            kw['shortcut'] = str(kw['shortcut'])[:SHORTCUT_MAX_LENGTH]
        # TODO: nechci nechat uzivatele zapisovat id,
        # potreba zajistit ve vsech resources
        kw.pop('id', None)
        kw['division'] = Division.get(division=kw['division']).id
        return super(Team, cls).create(*args, **kw)

    def set_attributes(self, **attributes):
        self.name = attributes.get('name', self.name)
        self.division = attributes.get('division', self.division)
        self.shortcut = attributes.get('shortcut', self.shortcut)
        self.city = attributes.get('city', self.city)
        self.country = attributes.get('country', self.country)
        self.user_id = attributes.get('user_id', self.user_id)
        self.cald_id = attributes.get('cald_id', self.cald_id)
