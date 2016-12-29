# #!/usr/bin/python
# # coding=utf-8

# -------------------------------------------------------------------------------------------------
# TODO: tady zacnu simulovat pozadavky rest api, naimportuju modely a budu volat jejich metody,
# TODO: aniz bych pouzil falcon nejakou dobu tedy nebudu potrebovat resources (falcon) ani uwsgi
# -------------------------------------------------------------------------------------------------
# TODO: psat testy na modely?
# -------------------------------------------------------------------------------------------------


# TODO: uzivateli pridam sloupec valid_to, ktery bude slouzit pro odhlasovani a platnosti api tokenu
# TODO: jmeno sloupce? validity? valid_to? api_key_valid_to?


# TODO: podivat se, jak by to slo udelat jinak
import pymysql
pymysql.install_as_MySQLdb()

# echo rika, ze provadi logging
from sqlalchemy import create_engine
engine = create_engine('mysql://:@localhost/catcher', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()




from sqlalchemy import Column, Integer, String

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    role = Column(String)

    def __repr__(self):
        return "<Role(id='%s', role='%s')>" % (
            self.id, self.role)


role = Role(id=4, role='test')

print(role)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()



for instance in session.query(Role).order_by(Role.id):
    print(instance.id, instance.role)


# for instance in session.query(Role).order_by(Role.role):
#     print(instance.id, instance.role)







# import requests
# import json
# from catcher import config
#
# # local  = "http://localhost:8080"
# # server = "http://catcher.zlutazimnice.cz"
# host   = config.app['host']
# print "HOST", host
#
# headers = {'content-type': "application/json", "Authorization": "nVFrrUXJSAXmTPp9lvZZLEyjiRVUydIQ"}
#
# # create 10 teams --------------------------------------------------------------------
#
# url = host + str("/api/teams/")
# # headers = {'content-type': "application/json"}
#
# print "VYTVARIM TYMY"
#
# payload = "{\"clubId\":1,\"divisionId\":1,\"degree\":\"A\"}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"clubId\":2,\"divisionId\":1,\"degree\":\"A\"}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"clubId\":3,\"divisionId\":1,\"degree\":\"A\"}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"clubId\":4,\"divisionId\":1,\"degree\":\"A\"}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"clubId\":5,\"divisionId\":1,\"degree\":\"A\"}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"clubId\":6,\"divisionId\":1,\"degree\":\"A\"}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"clubId\":8,\"divisionId\":1,\"degree\":\"A\"}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"clubId\":9,\"divisionId\":1,\"degree\":\"A\"}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"clubId\":10,\"divisionId\":1,\"degree\":\"A\"}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"clubId\":11,\"divisionId\":1,\"degree\":\"A\"}"
# response = requests.request("POST", url, data=payload, headers=headers)
#
# payload = "{\"clubId\":1,\"divisionId\":1,\"degree\":\"B\"}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"clubId\":1,\"divisionId\":2,\"degree\":\"A\"}"
# response = requests.request("POST", url, data=payload, headers=headers)
#
# # -------------------------------------------------
#
# tournament = '''{
#     "name": "PFL 2016",
#     "city": "Prague",
#     "country": "CZE",
#     "startDate": "2016-08-01",
#     "endDate": "2016-08-01",
#     "divisionId": 1,
#     "caldTournamentId": null,
#     "teams": [
#         {
#             "id": 1,
#             "seeding": 1
#         },
#         {
#             "id": 2,
#             "seeding": 2
#         },
#         {
#             "id": 3,
#             "seeding": 3
#         },
#         {
#             "id": 4,
#             "seeding": 4
#         }
#     ],
#     "fieldsCount": 1,
#     "fields": [
#         {
#             "id": 1,
#             "name": "Main field"
#         }
#     ],
#     "groups": [],
#     "playoff": [
#         {
#             "fieldId": 1,
#             "startTime": "2016-08-01T09:00:00",
#             "endTime": "2016-08-01T09:29:00",
#             "homeSeed": 1,
#             "awaySeed": 4,
#             "winner":{
#                     "nextStepIde": "FIN",
#                     "finalStanding": null
#                 },
#                 "looser":{
#                     "nextStepIde": "3RD",
#                     "finalStanding": null
#                 },
#             "ide": "SE1",
#             "description": null
#         },
#         {
#             "fieldId": 1,
#             "startTime": "2016-08-01T09:30:00",
#             "endTime": "2016-08-01T09:59:00",
#             "homeSeed": 2,
#             "awaySeed": 3,
#             "winner":{
#                     "nextStepIde": "FIN",
#                     "finalStanding": null
#                 },
#                 "looser":{
#                     "nextStepIde": "3RD",
#                     "finalStanding": null
#                 },
#             "ide": "SE2",
#             "description": null
#         },
#         {
#             "fieldId": 1,
#             "startTime": "2016-08-01T10:00:00",
#             "endTime": "2016-08-01T10:29:00",
#             "homeSeed": null,
#             "awaySeed": null,
#             "winner":{
#                     "nextStepIde": null,
#                     "finalStanding": 3
#                 },
#                 "looser":{
#                     "nextStepIde": null,
#                     "finalStanding": 4
#                 },
#             "ide": "3RD",
#             "description": null
#         },
#         {
#             "fieldId": 1,
#             "startTime": "2016-08-01T10:30:00",
#             "endTime": "2016-08-01T10:59:00",
#             "homeSeed": null,
#             "awaySeed": null,
#             "winner":{
#                     "nextStepIde": null,
#                     "finalStanding": 1
#                 },
#                 "looser":{
#                     "nextStepIde": null,
#                     "finalStanding": 2
#                 },
#             "ide": "FIN",
#             "description": "Finale"
#         }
#     ]
# }'''
#
# print "VYTVARIM TURNAJ"
#
# # create torunament --------------------------------------------------------------------
# url = host + str("/api/tournaments")
# r = requests.post(url, data=tournament, headers=headers)
# # print("Tournament", r.status_code, r.reason)
# try:
#     tournamentId = str(json.loads(r.text)['id'])
# except:
#     print r.text
# print "TOURNAMENT ID:", tournamentId
# # prepare tournament --------------------------------------------------------------------
#
# print "PREPARE TOURNAMENT"
#
# url = host + str("/api/tournament/" + tournamentId)
# payload = '{"ready":true}'
# response = requests.request("PUT", url, data=payload, headers=headers)
# if response.status_code != 200:
#     print("Tournaji nebyl nastaven priznak 'ready'")
#
#
# print "ROSTERS"
# # add players on rosters----------------------------------------------------------------
# url = host + str("/api/tournament/" + tournamentId + "/players")
# payload = "{\"playerId\":1,\"teamId\":1}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":2,\"teamId\":1}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":3,\"teamId\":1}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":4,\"teamId\":1}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":5,\"teamId\":1}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":6,\"teamId\":2}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":7,\"teamId\":2}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":8,\"teamId\":2}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":9,\"teamId\":2}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":10,\"teamId\":2}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":11,\"teamId\":3}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":12,\"teamId\":3}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":13,\"teamId\":3}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":14,\"teamId\":3}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":15,\"teamId\":3}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":16,\"teamId\":4}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":17,\"teamId\":4}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":18,\"teamId\":4}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":19,\"teamId\":4}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":20,\"teamId\":4}"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = "{\"playerId\":21,\"teamId\":4}"
# response = requests.request("POST", url, data=payload, headers=headers)
#
# # active tournament ---------------------------------------------------------------
# # url = host + str("/api/tournament/" + tournamentId)
# # payload = '{"active":true}'
# # headers = {'content-type': "application/json"}
# # response = requests.request("PUT", url, data=payload, headers=headers)
# # if response.status_code != 200:
# #     print("Tournaji nebyl nastaven priznak 'active'")
#
# print "ACTIVE MATCH"
#
# # active match --------------------------------------------------------------------
# url = host + str("/api/match/1")
# payload = '{"active":true, "description": "Semifinale 1"}'
# response = requests.request("PUT", url, data=payload, headers=headers)
# if response.status_code != 200:
#     print("Zapasu nebyl nastaven priznak 'active'")
#
# print "FIRST POINTS"
# # add points ----------------------------------------------------------------------
# url = host + str("/api/match/1/points")
# payload = "{\"assistPlayerId\": 1, \"scorePlayerId\": 2, \"homePoint\": true }"
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = '{"assistPlayerId": 16, "scorePlayerId":   17, "homePoint": false                   }'
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = '{                      "scorePlayerId":   17, "homePoint": false, "callahan": true }'
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = '{"assistPlayerId":  2, "scorePlayerId":    3, "homePoint": true                    }'
# response = requests.request("POST", url, data=payload, headers=headers)
# payload = '{"assistPlayerId": 18, "scorePlayerId": null, "homePoint": false                   }'
# response = requests.request("POST", url, data=payload, headers=headers)
# if response.status_code != 201:
#     print("Zapasu nebyl pridan bod")
#
# # ---------------------------------------------------------------------------------
#
# # TOURNAMENT 2
# tournament2 = '''{
#     "name": "Champions League 2016",
#     "city": "Prague",
#     "country": "CZE",
#     "startDate": "2016-08-01",
#     "endDate": "2016-08-01",
#     "divisionId": 1,
#     "caldTournamentId": null,
#     "teams": [{
#         "id": 1,
#         "seeding": 1
#     }, {
#         "id": 2,
#         "seeding": 2
#     }, {
#         "id": 3,
#         "seeding": 3
#     }, {
#         "id": 4,
#         "seeding": 4
#     }],
#     "fieldsCount": 1,
#     "fields": [{
#         "id": 1,
#         "name": "Main field"
#     }],
#     "groups": [{
#         "ide": "A",
#         "teams": [{
#             "id": 1
#         }, {
#             "id": 2
#         }],
#         "advancements": [{
#             "standing": 1,
#             "nextStepIde": "FIN",
#             "finalStanding": null
#         }, {
#             "standing": 2,
#             "nextStepIde": "3RD",
#             "finalStanding": null
#         }],
#         "matches": [{
#             "fieldId": 1,
#             "startTime": "2016-08-01T09:00:00",
#             "endTime": "2016-08-01T09:29:00",
#             "homeSeed": 1,
#             "awaySeed": 2,
#             "winner": {
#                 "nextStepIde": null,
#                 "finalStanding": null
#             },
#             "looser": {
#                 "nextStepIde": null,
#                 "finalStanding": null
#             },
#             "ide": "A1",
#             "description": null
#         }]
#     }, {
#         "ide": "B",
#         "teams": [{
#             "id": 3
#         }, {
#             "id": 4
#         }],
#         "advancements": [{
#             "standing": 1,
#             "nextStepIde": "FIN",
#             "finalStanding": null
#         }, {
#             "standing": 2,
#             "nextStepIde": "3RD",
#             "finalStanding": null
#         }],
#         "matches": [{
#             "fieldId": 1,
#             "startTime": "2016-08-01T09:30:00",
#             "endTime": "2016-08-01T09:59:00",
#             "homeSeed": 3,
#             "awaySeed": 4,
#             "winner": {
#                 "nextStepIde": null,
#                 "finalStanding": null
#             },
#             "looser": {
#                 "nextStepIde": null,
#                 "finalStanding": null
#             },
#             "ide": "B1",
#             "description": null
#         }]
#     }],
#
#     "playoff": [{
#         "fieldId": 1,
#         "startTime": "2016-08-01T10:00:00",
#         "endTime": "2016-08-01T10:29:00",
#         "homeSeed": null,
#         "awaySeed": null,
#         "winner": {
#             "nextStepIde": null,
#             "finalStanding": 3
#         },
#         "looser": {
#             "nextStepIde": null,
#             "finalStanding": 4
#         },
#         "ide": "3RD",
#         "description": null
#     }, {
#         "fieldId": 1,
#         "startTime": "2016-08-01T10:30:00",
#         "endTime": "2016-08-01T10:59:00",
#         "homeSeed": null,
#         "awaySeed": null,
#         "winner": {
#             "nextStepIde": null,
#             "finalStanding": 1
#         },
#         "looser": {
#             "nextStepIde": null,
#             "finalStanding": 2
#         },
#         "ide": "FIN",
#         "description": "Finale"
#     }]
# }
# '''
# # create torunament --------------------------------------------------------------------
# url = host + str("/api/tournaments")
# r = requests.post(url, data=tournament2, headers=headers)
# # print("Tournament", r.status_code, r.reason)
# try:
#     tournamentId = str(json.loads(r.text)['id'])
# except:
#     print r.text
# print "TOURNAMENT ID:", tournamentId
#
# # ready tournament ---------------------------------------------------------------------
# url = host + str("/api/tournament/" + tournamentId)
# payload = '{"ready":true}'
# response = requests.request("PUT", url, data=payload, headers=headers)
# if response.status_code != 200:
#     print("Tournaji nebyl nastaven priznak 'ready'")
#
# # play all matches ---------------------------------------------------------------------
#
# url = host + str("/api/match/5")
# payload = "{\"active\": true, \"terminated\": true, \"homeScore\": 1, \"awayScore\": 2 }"
# r = requests.put(url, data=payload, headers=headers)
# url = host + str("/api/match/6")
# payload = "{\"active\": true, \"terminated\": true, \"homeScore\": 4, \"awayScore\": 8 }"
# r = requests.put(url, data=payload, headers=headers)
# url = host + str("/api/match/7")
# payload = "{\"active\": true, \"terminated\": true, \"homeScore\": 0, \"awayScore\": 4 }"
# r = requests.put(url, data=payload, headers=headers)
# url = host + str("/api/match/8")
# payload = "{\"active\": true, \"terminated\": true, \"homeScore\": 11, \"awayScore\": 10 }"
# r = requests.put(url, data=payload, headers=headers)