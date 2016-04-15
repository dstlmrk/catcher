#!/usr/bin/python
# coding=utf-8

# from api.resource import Collection, Item
from catcher import models as m
# from tournamentCreater import TournamentCreater
import falcon
import logging
# import datetime
from catcher.models.queries import Queries
from playhouse.shortcuts import model_to_dict

class Sotg(object):

    def __init__(self, fair = None, communication = None, fouls = None, positive = None, rules = None):
        self.fair          = fair
        self.communication = communication
        self.fouls         = fouls
        self.positive      = positive
        self.rules         = rules
        self.total = None if fair is None else (fair + communication + fouls + positive + rules)

class Spirits(object):
    
    def on_get(self, req, resp, id):
        
        teamId = req.params.get('teamId')
        if teamId:
            qr = m.SpiritAvg.select().where(
                m.SpiritAvg.tournamentId == id,
                m.SpiritAvg.teamId == teamId
                ).dicts()
        else:
            qr = m.SpiritAvg.select().where(
                m.SpiritAvg.tournamentId == id
                ).dicts()
        
        spirits = []
        for spirit in qr:
            del spirit['matchesGiven'], spirit['tournamentId']
            spirits.append(spirit)
        
        collection = {
            'count'  : len(spirits),
            'spirits': spirits
        }
        req.context['result'] = collection

class Spirit(object):

    def getNewAvg(self, avg, matches, newValue, oldValue = None):
        if oldValue is None:
            return ((avg * matches) + newValue) / (matches + 1)
        else:
            return ((avg * matches) - oldValue + newValue) / (matches)

    def updateSpirit(self, matchId, data, put = False):
        
        logging.info("Match %s has new spirit" % matchId)

        match = m.Match.get(id=matchId)
        
        if not match.terminated:
            ValueError("Match is not terminated still")
        
        # check team ids
        receivingTeamId = int(data['teamId'])
        if receivingTeamId == match.homeTeamId:
            givingTeamId = match.awayTeamId
        elif receivingTeamId == match.awayTeamId:
            givingTeamId = match.homeTeamId
        else:
            raise ValueError("In match %s isn't team %s" % (match.id, receivingTeamId))

        # TODO: check rights, if user is giving team

        logging.info("Team %s gives spirit to team %s " % (givingTeamId, receivingTeamId))

        data['givingTeamId'] = givingTeamId

        newSotg = Sotg(
            data['fair'],
            data['communication'],
            data['fouls'],
            data['positive'],
            data['rules']
            )

        with m.db.transaction():

            # TODO: upravit spirit na prehledu zapasu!!! a otestovat

            oldSotg = Sotg()
            if put:
                # delete old spirit
                spirit = m.Spirit.get(
                    matchId = matchId, 
                    teamId = receivingTeamId
                    )
                oldSotg = Sotg(
                    spirit.fair,
                    spirit.communication,
                    spirit.fouls,
                    spirit.positive,
                    spirit.rules
                    )
                spirit.delete_instance()

            data['total'] = newSotg.total
            spirit, created = m.Spirit.get_or_create(
                matchId = matchId,
                teamId  = receivingTeamId,
                defaults = data
                )
            logging.info("spirit: %s" % (spirit))

            # given ---------------------------------------------------------------

            spiritAvg = m.SpiritAvg.get(
                tournamentId = match.tournamentId,
                teamId = givingTeamId
                )

            spiritAvg.communicationGiven = self.getNewAvg(
                spiritAvg.communicationGiven,
                spiritAvg.matchesGiven,
                newSotg.communication,
                oldSotg.communication
                )
            spiritAvg.fairGiven = self.getNewAvg(
                spiritAvg.fairGiven,
                spiritAvg.matchesGiven,
                newSotg.fair,
                oldSotg.fair
                )
            spiritAvg.foulsGiven = self.getNewAvg(
                spiritAvg.foulsGiven,
                spiritAvg.matchesGiven,
                newSotg.fouls,
                oldSotg.fouls
                )
            spiritAvg.positiveGiven = self.getNewAvg(
                spiritAvg.positiveGiven,
                spiritAvg.matchesGiven,
                newSotg.positive,
                oldSotg.positive
                )
            spiritAvg.rulesGiven = self.getNewAvg(
                spiritAvg.rulesGiven,
                spiritAvg.matchesGiven,
                newSotg.rules,
                oldSotg.rules
                )
            spiritAvg.totalGiven = self.getNewAvg(
                spiritAvg.totalGiven,
                spiritAvg.matchesGiven,
                newSotg.total,
                oldSotg.total
                )
            if not put:
                spiritAvg.matchesGiven = (spiritAvg.matchesGiven + 1)

            spiritAvg.save()

            # received ------------------------------------------------------------

            spiritAvg = m.SpiritAvg.get(
                tournamentId = match.tournamentId,
                teamId = receivingTeamId
                )

            spiritAvg.communication = self.getNewAvg(
                spiritAvg.communication,
                spiritAvg.matches,
                newSotg.communication,
                oldSotg.communication
                )
            spiritAvg.fair = self.getNewAvg(
                spiritAvg.fair,
                spiritAvg.matches,
                newSotg.fair,
                oldSotg.fair
                )
            spiritAvg.fouls = self.getNewAvg(
                spiritAvg.fouls,
                spiritAvg.matches,
                newSotg.fouls,
                oldSotg.fouls
                )
            spiritAvg.positive = self.getNewAvg(
                spiritAvg.positive,
                spiritAvg.matches,
                newSotg.positive,
                oldSotg.positive
                )
            spiritAvg.rules = self.getNewAvg(
                spiritAvg.rules,
                spiritAvg.matches,
                newSotg.rules,
                oldSotg.rules
                )
            spiritAvg.total = self.getNewAvg(
                spiritAvg.total,
                spiritAvg.matches,
                newSotg.total,
                oldSotg.total
                )
            if not put:
                spiritAvg.matches = (spiritAvg.matches + 1)

            spiritAvg.save()

            if match.homeTeamId == receivingTeamId:
                match.spiritHome = newSotg.total
            else:
                match.spiritAway = newSotg.total
            match.save()
            # ---------------------------------------------------------------------

        return spirit, created

    def on_get(self, req, resp, id):
        # napsat get pro nejake souhrne hodnoceni
        match = Queries.getMatches(matchId=id)[0]
        homeSpirit = None
        awaySpirit = None

        try:
            homeSpirit = model_to_dict(m.Spirit.get(matchId = id, teamId = match['homeTeam']['id']))
            del homeSpirit['matchId'], homeSpirit['teamId'], homeSpirit['givingTeamId']
        except m.Spirit.DoesNotExist:
            pass
        finally:
            match['homeTeam']['spirit'] = homeSpirit

        try:
            awaySpirit = model_to_dict(m.Spirit.get(matchId = id, teamId = match['awayTeam']['id']))
            del awaySpirit['matchId'], awaySpirit['teamId'], awaySpirit['givingTeamId']
        except m.Spirit.DoesNotExist:
            pass
        finally:
            match['awayTeam']['spirit'] = awaySpirit

        req.context['result'] = match

    def on_put(self, req, resp, id):
        match = m.Match.get(id=id)
        tournament = m.Tournament.get(id=match.tournamentId)
        if tournament.terminated:
            raise ValueError("Tournament is terminated")
        spirit, created = self.updateSpirit(int(id), req.context['data'], True)
        resp.status = falcon.HTTP_200 if created else falcon.HTTP_304
        req.context['result'] = spirit

    # /api/match/{id}/spirit
    def on_post(self, req, resp, id):
        spirit, created = self.updateSpirit(int(id), req.context['data'])
        resp.status = falcon.HTTP_201 if created else falcon.HTTP_200
        req.context['result'] = spirit