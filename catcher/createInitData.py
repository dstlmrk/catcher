#!/usr/bin/python
# coding=utf-8

import models
import requests

models.db.connect()

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

if not models.db.is_closed():
    models.db.close()
# -------------------------------------------------

tournament = '''{
    "name": "PFL 2016",
    "city": "Prague",
    "country": "CZE",
    "startDate": "2016-04-01",
    "endDate": "2016-04-01",
    "division": 1,
    "caldTournament": null,
    "teams": [
        {
            "id": 1,
            "seeding": 1
        },
        {
            "id": 2,
            "seeding": 2
        },
        {
            "id": 3,
            "seeding": 3
        },
        {
            "id": 4,
            "seeding": 4
        }
    ],
    "fieldsCount": 1,
    "fields": [
        {
            "id": 1,
            "name": "Main field"
        }
    ],
    "groups": [],
    "matches": [
        {
            "field": 1,
            "startTime": "2016-04-01T09:00:00",
            "endTime": "2016-04-01T09:29:00",
            "homeSeed": 1,
            "awaySeed": 4,
            "looserNextStep": "3RD",
            "winnerNextStep": "FIN",
            "looserFinalStanding": null,
            "winnerFinalStanding": null,
            "identificator": "SE1",
            "description": null
        },
        {
            "field": 1,
            "startTime": "2016-04-01T09:30:00",
            "endTime": "2016-04-01T09:59:00",
            "homeSeed": 2,
            "awaySeed": 3,
            "looserNextStep": "3RD",
            "winnerNextStep": "FIN",
            "looserFinalStanding": null,
            "winnerFinalStanding": null,
            "identificator": "SE2",
            "description": null
        },
        {
            "field": 1,
            "startTime": "2016-04-01T10:00:00",
            "endTime": "2016-04-01T10:29:00",
            "homeSeed": null,
            "awaySeed": null,
            "looserNextStep": null,
            "winnerNextStep": null,
            "looserFinalStanding": 4,
            "winnerFinalStanding": 3,
            "identificator": "3RD",
            "description": null
        },
        {
            "field": 1,
            "startTime": "2016-04-01T10:30:00",
            "endTime": "2016-04-01T10:59:00",
            "homeSeed": null,
            "awaySeed": null,
            "looserNextStep": null,
            "winnerNextStep": null,
            "looserFinalStanding": 2,
            "winnerFinalStanding": 1,
            "identificator": "FIN",
            "description": "Finale"
        }
    ]
}'''


url = "http://localhost:8080/api/tournaments/create"
headers = {'content-type': 'application/json'}
r = requests.post(url, data=tournament, headers=headers)
print("Tournament", r.status_code, r.reason)