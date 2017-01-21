#!/usr/bin/python
# coding=utf-8

import falcon
from abc import abstractmethod, ABCMeta


class Privilege(object):
    """
    Abstract class that controls user privileges.
    """
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

# TODO: IsOwner?

class HasRole(Privilege):
    """
    Class that controls user role.
    """

    def __init__(self, roles):
        if not isinstance(roles, list):
            roles = [roles]
        self.roles = roles

    def evaluate(self, req, resp, resource, params):
        user = req.context["user"]
        # TODO: az tady budu vracet prihlaseneho uzivatele, je potreba overit jeho roli
        return user.role in self.roles


class IsLoggedUser(Privilege):
    """
    Class that controls logged users.
    """
    def evaluate(self, req, resp, resource, params):
        user = req.context["user"]
        return bool(user.id)


class IsThatUser(Privilege):
    """"""

    def evaluate(self, req, resp, resource, params):
        # TODO: tady se mi to nejak nezda, az tuhle funkcionalitu budu potrebovat, tak pozor!
        user = req.context["user"]
        user_id = req.get_param_as_int("id", True)
        return user.id == user_id
