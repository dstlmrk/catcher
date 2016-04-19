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
from catcher.api.privileges import Privilege

class Sotg(object):

    @staticmethod
    def checkValue(value):
        if value is None or 0 <= value <= 4:
            return value
        else:
            raise falcon.HTTPBadRequest("Invalid spirit", "Incorrect values")

    def __init__(self, fair = None, communication = None, fouls = None, positive = None, rules = None):
        self.fair          = Sotg.checkValue(fair)
        self.communication = Sotg.checkValue(communication)
        self.fouls         = Sotg.checkValue(fouls)
        self.positive      = Sotg.checkValue(positive)
        self.rules         = Sotg.checkValue(rules)
        self.total = None if fair is None else (fair + communication + fouls + positive + rules)

class Spirits(object):
    
    def on_get(self, req, resp, id):
        tournament = m.Tournament.get(id=id)
        if not tournament.terminated:
            raise falcon.HTTPBadRequest(
                "Tournament isn't terminated yet",
                "Spirits are visible after tournament"
                )

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
            'count': len(spirits),
            'items': spirits
        }
        req.context['result'] = collection

class MissingSpirits(object):

    @falcon.before(Privilege(["organizer", "admin"]))
    def on_get(self, req, resp, id):
        Privilege.checkOrganizer(req.context['user'], int(id))
        tournament = m.Tournament.get(id=id)
        matches = Queries.getMatches(tournamentId=id)

        missingSpirits = []
        for match in matches:
            if match['terminated'] != True:
                continue
            if match['homeTeam']['spirit'] is None:
                missingSpirits.append({
                    'teamId'       : match['homeTeam']['id'],
                    'teamName'     : match['awayTeam']['name'],
                    'matchId'      : match['id'],
                    'identificator': match['identificator']
                    })
            if match['awayTeam']['spirit'] is None:
                missingSpirits.append({
                    'teamId'       : match['homeTeam']['id'],
                    'teamName'     : match['homeTeam']['name'],
                    'matchId'      : match['id'],
                    'identificator': match['identificator']
                    }) 

        collection = {
            'count': len(missingSpirits),
            'items': missingSpirits
        }
        req.context['result'] = collection





class Spirit(object):

    def getGivingTeamId(self, receivingTeamId, match):
        if receivingTeamId == match.homeTeamId:
            return match.awayTeamId
        elif receivingTeamId == match.awayTeamId:
            return match.homeTeamId
        else:
            raise ValueError("In match %s isn't team %s" % (match.id, receivingTeamId))

    def getNewAvg(self, avg, matches, newValue, oldValue = None):
        if oldValue is None:
            return ((avg * matches) + newValue) / (matches + 1)
        else:
            return ((avg * matches) - oldValue + newValue) / (matches)

    def updateSpirit(self, matchId, data, user, put = False):
        logging.info("Match %s has new spirit" % matchId)

        match = m.Match.get(id=matchId)
        tournament = m.Tournament.get(id=match.tournamentId)

        if tournament.terminated:
            raise ValueError("Tournament is terminated")
        
        if not match.terminated:
            raise ValueError("Match is not terminated still")
        
        # check team ids
        receivingTeamId = int(data['teamId'])
        givingTeamId = self.getGivingTeamId(receivingTeamId, match)

        # check rights, if user is giving team
        Privilege.checkOrganizer(user, match.tournamentId)
        team = m.Team.get(id=givingTeamId)
        Privilege.checkClub(user, team.clubId)


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

    @falcon.before(Privilege(["club", "organizer", "admin"]))
    def on_get(self, req, resp, id):
        loggedUser = req.context['user']
        match = Queries.getMatches(matchId=id)[0]
        Privilege.checkOrganizer(loggedUser, m.Match.get(id=id).tournamentId)
        
        homeSpirit = None
        awaySpirit = None
        try:
            homeSpirit = model_to_dict(m.Spirit.get(matchId = id, teamId = match['homeTeam']['id']))
            del homeSpirit['matchId'], homeSpirit['teamId'], homeSpirit['givingTeamId']
            # if spirit is not club's
            team = m.Team.get(id=match['homeTeam']['id'])
            if loggedUser.role =="club" and not loggedUser.clubId ==  team.clubId:
                homeSpirit = None
        except m.Spirit.DoesNotExist:
            pass
        finally:
            match['homeTeam']['spirit'] = homeSpirit

        try:
            awaySpirit = model_to_dict(m.Spirit.get(matchId = id, teamId = match['awayTeam']['id']))
            del awaySpirit['matchId'], awaySpirit['teamId'], awaySpirit['givingTeamId']
            # if spirit is not club's
            team = m.Team.get(id=match['awayTeam']['id'])
            if loggedUser.role =="club" and not loggedUser.clubId ==  team.clubId:
                homeSpirit = None
        except m.Spirit.DoesNotExist:
            pass
        finally:
            match['awayTeam']['spirit'] = awaySpirit

        req.context['result'] = match

    @falcon.before(Privilege(["club", "organizer", "admin"])) 
    def on_put(self, req, resp, id):
        spirit, created = self.updateSpirit(int(id), req.context['data'], req.context['user'], True)
        resp.status = falcon.HTTP_200 if created else falcon.HTTP_304
        req.context['result'] = spirit

    @falcon.before(Privilege(["club", "organizer", "admin"]))
    def on_post(self, req, resp, id):
        spirit, created = self.updateSpirit(int(id), req.context['data'], req.context['user'])
        resp.status = falcon.HTTP_201 if created else falcon.HTTP_200
        req.context['result'] = spirit