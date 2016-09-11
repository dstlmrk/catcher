#!/usr/bin/python
# coding=utf-8

import logging
import falcon
from catcher import models


class Login(object):

    def on_post(self, req, resp):
        '''check login'''
        try:
            user = models.User.login(
                **req.context['data']
            )
            user.password = None
            req.context['result'] = user
        except:
            raise falcon.HTTPUnauthorized(
                "Authentication Failed",
                "Email or password is wrong."
            )


class ForgottenPassword(object):

    def on_post(self, req, resp):
        '''send new password'''
        email = req.params['email']
        try:
            user = models.User.get(email=email)
        except User.DoesNotExist:
            # TODO: mel bych vracet OK, protoze potvrzeni chodi na email
            raise falcon.HTTPBadRequest(
                "Bad input",
                "User with email %s doesn't exist" % email
            )
        models.Login.resetPassword(user)
