#!/usr/bin/python
# coding=utf-8

import falcon
from abc import abstractmethod, ABCMeta
from catcher.logger import logger
from catcher.models.base import _session
from catcher.models import Tournament


class Privilege(object):
    """Abstract class that checks user privileges"""
    __meta__ = ABCMeta

    @abstractmethod
    def evaluate(self, req, resp, resource, params):
        return True

    def __call__(self, req, resp, resource, params):
        # v before nema request nastaveny jeste params (nevim, zda je to nutne)
        # req._params.update(params)
        if not self.evaluate(req, resp, resource, params):
            raise falcon.HTTPUnauthorized(
                "Authentication Required", (
                    "This server could not verify that "
                    "you are authorized to access the document requested."
                )
            )


class HasRole(Privilege):
    """Checks user role"""

    def __init__(self, roles):
        if not isinstance(roles, list):
            roles = [roles]
        self.roles = roles

    def evaluate(self, req, resp, resource, params):
        user = req.context["user"]
        return user.role.type in self.roles


class IsOwner(Privilege):
    """Checks if user is owner of the object"""

    def __init__(self, model):
        self.model = model

    def evaluate(self, req, resp, resource, params):
        user = req.context["user"]
        obj = _session.query(self.model).get(params.get('id'))
        if hasattr(obj, "user_id"):
            return obj.user_id == user.id
        if hasattr(obj, "tournament_id"):
            tournament = _session.query(Tournament).get(obj.tournament_id)
            return tournament.user_id == user.id
        return False


class IsLoggedUser(Privilege):
    """Checks if user is logged"""

    def evaluate(self, req, resp, resource, params):
        user = req.context["user"]
        return bool(user.id)


class IsThatUser(Privilege):
    """Checks if user works with himself"""

    def evaluate(self, req, resp, resource, params):
        user = req.context["user"]
        return user.id == int(params.get('id'))


class LogicPrivilege(Privilege):

    def __init__(self, privilege_a, privilege_b):
        self.privilege_a = privilege_a
        self.privilege_b = privilege_b

    def evaluate(self, req, resp, resource, params):
        super(LogicPrivilege, self).evaluate()


class AndPrivilege(LogicPrivilege):

    def evaluate(self, req, resp, resource, params):
        return self.privilege_a.evaluate(req, resp, resource, params) \
               and self.privilege_b.evaluate(req, resp, resource, params)


class OrPrivilege(LogicPrivilege):

    def evaluate(self, req, resp, resource, params):
        return self.privilege_a.evaluate(req, resp, resource, params) \
               or self.privilege_b.evaluate(req, resp, resource, params)
