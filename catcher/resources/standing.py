#!/usr/bin/python
# coding=utf-8

from catcher import models as m
from playhouse.shortcuts import model_to_dict

class Standings(object):

    def on_get(self, req, resp, id):
        tournament = m.Tournament.get(id=id)

        if not tournament.ready:
            raise ValueError("Tournament hasn't started yet")

        qr = m.Standing.select().where(
                m.Standing.tournamentId == id
            ).order_by(
                m.Standing.standing.asc()
            )
        standings = []
        for standing in qr:
            standings.append(standing.json)

        spirits = []
        if tournament.terminated:
            qr = m.SpiritAvg.select().where(
                    m.SpiritAvg.tournamentId == id
                ).order_by(
                    m.SpiritAvg.total.desc()
                )
            for spirit in qr:
                # spirit = model_to_dict(spirit)
                spirit = {
                    "total"     : spirit.total,
                    "teamId"    : spirit.teamId,
                    "matches"   : spirit.matches,
                    "totalGiven": spirit.totalGiven
                    } 
                # del spiritspirit['matchesGiven']
                # del spirit['tournamentId']
                spirits.append(spirit)
        else:
            spirits = None

        collection = {
            'teams'     : len(standings),
            'standings' : standings,
            'spirits'   : spirits
            }
        req.context['result'] = collection