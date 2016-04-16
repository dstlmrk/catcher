#!/usr/bin/python
# coding=utf-8

from catcher import models as m
from playhouse.shortcuts import model_to_dict

class Standings(object):

    def on_get(self, req, resp, id):
        tournament = m.Tournament.select(
                m.Tournament.ready,
                m.Tournament.terminated
            ).where(
                m.Tournament.id == id
            ).get()

        if not tournament.ready and not tournament.terminated:
            raise ValueError("Tournament hasn't any standings")

        qr = m.Standing.select().where(
                m.Standing.tournamentId == id
            ).order_by(
                m.Standing.standing.asc()
            )
        standings = []
        for standing in qr:
            standings.append(standing.json)

        # TODO: pouze, pokud na to ma pravo nebo turnaj neni je terminated

        spirits = []
        if tournament.terminated:
            qr = m.SpiritAvg.select().where(
                    m.SpiritAvg.tournamentId == id
                ).order_by(
                    m.SpiritAvg.total.desc()
                )
            for spirit in qr:
                spirit = model_to_dict(spirit)
                del spirit['matchesGiven']
                del spirit['tournamentId']
                spirits.append(spirit)
        else:
            spirits = None

        collection = {
            'teams'     : len(standings),
            'standings' : standings,
            'spirits'   : spirits
            }
        req.context['result'] = collection



        {
    "standings": [{
        "standing": 1,
        "teamId": 3
    }, {
        "standing": 2,
        "teamId": 4
    }, {
        "standing": 3,
        "teamId": 2
    }, {
        "standing": 4,
        "teamId": 1
    }], "spirits": [{
        "foulsGiven": 2.0,
        "fair": 4.0,
        "totalGiven": 10.0,
        "matches": 2,
        "communication": 2.0,
        "communicationGiven": 2.0,
        "rulesGiven": 2.0,
        "fairGiven": 2.0,
        "fouls": 1.0,
        "teamId": 1,
        "rules": 3.0,
        "positiveGiven": 2.0,
        "total": 12.0,
        "positive": 2.0
    }, {
        "foulsGiven": 1.5,
        "fair": 3.0,
        "totalGiven": 11.0,
        "matches": 2,
        "communication": 2.0,
        "communicationGiven": 2.0,
        "rulesGiven": 2.5,
        "fairGiven": 3.0,
        "fouls": 1.5,
        "teamId": 2,
        "rules": 2.5,
        "positiveGiven": 2.0,
        "total": 11.0,
        "positive": 2.0
    }, {
        "foulsGiven": 1.5,
        "fair": 3.0,
        "totalGiven": 11.0,
        "matches": 2,
        "communication": 2.0,
        "communicationGiven": 2.0,
        "rulesGiven": 2.5,
        "fairGiven": 3.0,
        "fouls": 1.5,
        "teamId": 4,
        "rules": 2.5,
        "positiveGiven": 2.0,
        "total": 11.0,
        "positive": 2.0
    }, {
        "foulsGiven": 1.0,
        "fair": 2.0,
        "totalGiven": 12.0,
        "matches": 2,
        "communication": 2.0,
        "communicationGiven": 2.0,
        "rulesGiven": 3.0,
        "fairGiven": 4.0,
        "fouls": 2.0,
        "teamId": 3,
        "rules": 2.0,
        "positiveGiven": 2.0,
        "total": 10.0,
        "positive": 2.0
    }], "teams": 4
}