#!/usr/bin/python
# coding=utf-8

from catcher import models as m
from catcher.api.privileges import *
import falcon
import uuid
import re
import peewee as pw



class Users(object):

    @classmethod
    def getFreeApiKey(cls):
        for i in range(10):
            apiKey = uuid.uuid4().hex
            try:
                m.User.get(apiKey=apiKey)
            except m.User.DoesNotExist:
                return apiKey
            else:
                continue
        raise falcon.HTTPServiceUnavailable(
            "Try it again",
            "Catcher couldn't generate new api key, please try it again"
            )

    @classmethod
    def checkData(cls, email, password, role):
        # validate password
        if not len(password) > 5:
            raise ValueError("Password is too much short")
        if not password.isalnum():
            raise ValueError("Password in't alphanumeric")
        # validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email format is invalid")
        # validate role
        if role not in ["organizer", "club"]:
            raise ValueError(
                "Role %s is not supported" % role
                )

    @classmethod
    def createClubUser(cls, data, apiKey):
        newId = m.User(
            apiKey = apiKey,
            **data
            ).save()

    @classmethod
    def createOrganizerUser(cls, data, apiKey):
        if 'clubId' in data:
            del data['clubId']
        newId = m.User(
            apiKey = apiKey,
            **data
            ).save()

    # @falcon.before(Privilege("admin"))
    def on_post(self, req, resp):
        '''create new user'''
        data = req.context['data']

        Users.checkData(data['email'], data['password'], data['role'])
        apiKey = Users.getFreeApiKey()

        if data['role'] == "organizer":
            Users.createOrganizerUser(data, apiKey)
        elif data['role'] == "club":
            if req.context['user'].role == "admin":
                Users.createClubUser(data, apiKey)
        else:
            raise ValueError(
                "Role %s is not supported" % role
                )

        req.context['result'] = m.User.get(apiKey=apiKey)
        resp.status = falcon.HTTP_201






        # TODO: zatim se muzes registrovat pouze uzivatel s roli organizer
        # ---------------------------

        # TODO: vytvorit noveho uzivatele s unikatnim club_id, emailem, heslem
        # zapsat do tabaze jeho roli a vsechno posefovat

class User(object):

    def on_put(self, req, resp):
        '''edit user data and set new password'''
        # TODO: only for logged users