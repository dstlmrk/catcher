#!/usr/bin/python
# coding=utf-8

import models

# create divisions --------------------------------
divisions = [
    {"division": "open"},
    {"division": "women"},
    {"division": "mixed"},
    {"division": "masters"},
    {"division": "junior"},
    ]
try:
    models.Division.insert_many(divisions).execute()
except models.pw.IntegrityError as ex:
    pass

# create 10 teams ---------------------------------
teams = [
    {
    "club"     : 1,
    "division" : 1,
    "degree"   : "A"
    }
    ,{
    "club"     : 2,
    "division" : 1,
    "degree"   : "A"
    },{
    "club"     : 3,
    "division" : 1,
    "degree"   : "A"
    },{
    "club"     : 4,
    "division" : 1,
    "degree"   : "A"
    },{
    "club"     : 5,
    "division" : 1,
    "degree"   : "A"
    },{
    "club"     : 6,
    "division" : 1,
    "degree"   : "A"
    },{
    "club"     : 7,
    "division" : 1,
    "degree"   : "A"
    },{
    "club"     : 8,
    "division" : 1,
    "degree"   : "A"
    },{
    "club"     : 9,
    "division" : 1,
    "degree"   : "A"
    },{
    "club"     : 10,
    "division" : 1,
    "degree"   : "A"
    }
    ]
try:
    models.Team.insert_many(teams).execute()
except models.pw.IntegrityError as ex:
    pass
    
# create 10 teams ---------------------------------