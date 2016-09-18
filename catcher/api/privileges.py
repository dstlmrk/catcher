#!/usr/bin/python
# coding=utf-8

import falcon
from abc import abstractmethod, ABCMeta
# from catcher import models as m


class Privilege(object):
    __meta__ = ABCMeta

    @abstractmethod
    def evaluate(self, req, resp, resource, params):
        return True

    # def evaluate(self, req, resp, resource, params):
    #     user = req.context["user"]
    #     return user.role in self.roles

    def __call__(self, req, resp, resource, params):
        # v before nema request nastaveny jeste params (nevim, zda je to nutne)
        # req._params.update(params)
        if not self.evaluate(req, resp, resource, params):
            # raise Exception
            raise falcon.HTTPUnauthorized(
                "Authentication Required", (
                    "This server could not verify that "
                    "you are authorized to access the document requested."
                )
            )

#     @staticmethod
#     def checkUser(loggedUser, userId):
#         if loggedUser.id != userId:
#             Privilege.raise401()

#     @staticmethod
#     def checkClub(loggedUser, clubId):
#         if clubId is None:
#             return
#         if loggedUser.role == "club" and loggedUser.clubId != clubId:
#             Privilege.raise401()

#     @staticmethod
#     def checkOrganizer(loggedUser, tournamentId):
#         if tournamentId is None:
#             return
#         if loggedUser.role == "organizer":
#             try:
#                 m.Tournament.get(
#                     userId = loggedUser.id,
#                     id = tournamentId
#                     )
#             except m.Tournament.DoesNotExist:
#                 Privilege.raise401()


class HasRole(Privilege):
    def __init__(self, roles):
        if not isinstance(roles, list):
            roles = [roles]
        self.roles = roles

    def evaluate(self, req, resp, resource, params):
        user = req.context["user"]
        print "=================="
        print user.role.role
        return user.role.role in self.roles


class IsLoggedUser(Privilege):
    def evaluate(self, req, resp, resource, params):
        user = req.context["user"]
        return bool(user.id)


class IsThatUser(Privilege):
    def evaluate(self, req, resp, resource, params):
        user = req.context["user"]
        userId = req.get_param_as_int("id", True)
        return user.id == userId
