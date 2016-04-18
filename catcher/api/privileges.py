#!/usr/bin/python
# coding=utf-8

import falcon
from catcher import models as m

class Privilege(object):
    
    def __init__(self, roles):
        if not isinstance(roles, list):
            roles = [roles]
        self.roles = roles

    def evaluate(self, req, resp, resource, params):
        user = req.context["user"]
        return user.role in self.roles

    def __call__(self, req, resp, resource, params):
        if not self.evaluate(req, resp, resource, params):
            Privilege.raise401()

    @staticmethod
    def checkUser(loggedUser, userId):
        if loggedUser.id != userId:
            Privilege.raise401()

    @staticmethod
    def checkClub(loggedUser, clubId):
        if clubId is None:
            return
        if loggedUser.role == "club" and loggedUser.clubId != clubId:
            Privilege.raise401()

    @staticmethod
    def checkOrganizer(loggedUser, tournamentId):
        if tournamentId is None:
            return
        if loggedUser.role == "organizer":
            try:
                m.OrganizerHasTournament.get(
                    userId = loggedUser.id,
                    tournamentId = tournamentId
                    )
            except m.OrganizerHasTournament.DoesNotExist:
                Privilege.raise401()

    @classmethod
    def raise401(cls):
        raise falcon.HTTPUnauthorized(
                "Authentication Required",
                ("This server could not verify that "
                "you are authorized to access the document requested.")
            )