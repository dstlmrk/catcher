#!/usr/bin/python
# coding=utf-8

import models
import requests
import json
from catcher import config

# local  = "http://localhost:8080"
# server = "http://catcher.zlutazimnice.cz"
host   = config.app['host']
print "HOST", host

# create 10 teams --------------------------------------------------------------------

url = host + str("/api/teams/")
headers = {'content-type': "application/json"}

payload = "{\"clubId\":1,\"divisionId\":1,\"degree\":\"A\"}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"clubId\":2,\"divisionId\":1,\"degree\":\"A\"}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"clubId\":3,\"divisionId\":1,\"degree\":\"A\"}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"clubId\":4,\"divisionId\":1,\"degree\":\"A\"}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"clubId\":5,\"divisionId\":1,\"degree\":\"A\"}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"clubId\":6,\"divisionId\":1,\"degree\":\"A\"}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"clubId\":8,\"divisionId\":1,\"degree\":\"A\"}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"clubId\":9,\"divisionId\":1,\"degree\":\"A\"}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"clubId\":10,\"divisionId\":1,\"degree\":\"A\"}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"clubId\":11,\"divisionId\":1,\"degree\":\"A\"}"
response = requests.request("POST", url, data=payload, headers=headers)

payload = "{\"clubId\":1,\"divisionId\":1,\"degree\":\"B\"}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"clubId\":1,\"divisionId\":2,\"degree\":\"A\"}"
response = requests.request("POST", url, data=payload, headers=headers)

# -------------------------------------------------

tournament = '''{
    "name": "PFL 2016",
    "city": "Prague",
    "country": "CZE",
    "startDate": "2016-04-01",
    "endDate": "2016-04-01",
    "divisionId": 1,
    "caldTournamentId": null,
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
            "fieldId": 1,
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
            "fieldId": 1,
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
            "fieldId": 1,
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
            "fieldId": 1,
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

# create torunament --------------------------------------------------------------------
url = host + str("/api/tournaments")
headers = {'content-type': 'application/json'}
r = requests.post(url, data=tournament, headers=headers)
# print("Tournament", r.status_code, r.reason)
tournamentId = str(json.loads(r.text)['id'])
print "TOURNAMENT ID:", tournamentId
# prepare tournament --------------------------------------------------------------------
url = host + str("/api/tournament/" + tournamentId)
payload = '{"ready":true}'
headers = {'content-type': "application/json"}
response = requests.request("PUT", url, data=payload, headers=headers)
if response.status_code != 200:
    print("Tournaji nebyl nastaven priznak 'ready'")

# add players on rosters----------------------------------------------------------------
url = host + str("/api/tournament/" + tournamentId + "/players")
headers = {'content-type': "application/json"}
payload = "{\"playerId\":1,\"teamId\":1}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":2,\"teamId\":1}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":3,\"teamId\":1}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":4,\"teamId\":1}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":5,\"teamId\":1}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":6,\"teamId\":2}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":7,\"teamId\":2}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":8,\"teamId\":2}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":9,\"teamId\":2}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":10,\"teamId\":2}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":11,\"teamId\":3}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":12,\"teamId\":3}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":13,\"teamId\":3}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":14,\"teamId\":3}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":15,\"teamId\":3}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":16,\"teamId\":4}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":17,\"teamId\":4}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":18,\"teamId\":4}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":19,\"teamId\":4}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":20,\"teamId\":4}"
response = requests.request("POST", url, data=payload, headers=headers)
payload = "{\"playerId\":21,\"teamId\":4}"
response = requests.request("POST", url, data=payload, headers=headers)

# active tournament ---------------------------------------------------------------
# url = host + str("/api/tournament/" + tournamentId)
# payload = '{"active":true}'
# headers = {'content-type': "application/json"}
# response = requests.request("PUT", url, data=payload, headers=headers)
# if response.status_code != 200:
#     print("Tournaji nebyl nastaven priznak 'active'")

# active match --------------------------------------------------------------------
url = host + str("/api/match/1")
payload = '{"active":true, "description": "Semifinale 1"}'
headers = {'content-type': "application/json"}
response = requests.request("PUT", url, data=payload, headers=headers)
if response.status_code != 200:
    print("Zapasu nebyl nastaven priznak 'active'")

# add points ----------------------------------------------------------------------
url = host + str("/api/match/1/points")
headers = {'content-type': "application/json"}
payload = "{\"assistPlayerId\": 1, \"scorePlayerId\": 2, \"homePoint\": true }"
response = requests.request("POST", url, data=payload, headers=headers)
payload = '{"assistPlayerId": 16, "scorePlayerId":   17, "homePoint": false                   }'
response = requests.request("POST", url, data=payload, headers=headers)
payload = '{                      "scorePlayerId":   17, "homePoint": false, "callahan": true }'
response = requests.request("POST", url, data=payload, headers=headers)
payload = '{"assistPlayerId":  2, "scorePlayerId":    3, "homePoint": true                    }'
response = requests.request("POST", url, data=payload, headers=headers)
payload = '{"assistPlayerId": 18, "scorePlayerId": null, "homePoint": false                   }'
response = requests.request("POST", url, data=payload, headers=headers)
if response.status_code != 201:
    print("Zapasu nebyl pridan bod")

# --------------------------------------------------------------------------------- 