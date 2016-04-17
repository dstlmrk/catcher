#!/usr/bin/python
# coding=utf-8

import falcon

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
            raise falcon.HTTPUnauthorized(
                "Authentication Required",
                ("This server could not verify that "
                "you are authorized to access the document requested.")
            )