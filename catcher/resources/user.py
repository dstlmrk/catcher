#!/usr/bin/python
# coding=utf-8

from catcher import models as m
from catcher.api.privileges import Privilege
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
        Users.checkPassword(password)
        Users.checkEmail(email)
        # validate role
        if role not in ["organizer", "club"]:
            raise ValueError(
                "Role %s is not supported" % role
                )

    @staticmethod
    def checkEmail(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email format is invalid")

    @staticmethod
    def checkPassword(password):
        if not len(password) > 5:
            raise ValueError("Password is too much short")
        if not password.isalnum():
            raise ValueError("Password in't alphanumeric")

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

    # TODO: zatim se muzes registrovat pouze uzivatel s roli organizer
    # admin muze zaregistrovat club
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

class User(object):

    @falcon.before(Privilege(["club", "organizer", "admin"]))
    def on_put(self, req, resp, id):
        '''edit user data and set new password'''
        Privilege.checkUser(req.context['user'], int(id))

        data = req.context['data']
        user = m.User.get(id=id)

        if 'email' in data:
            Users.checkEmail(data['email'])
            user.email = data['email']

        if 'newPassword' in data:
            if 'oldPassword' in data:
                Users.checkPassword(data['newPassword'])
                if data['oldPassword'] == user.password:
                    user.password = data['newPassword']
                else:
                    raise ValueError("Password is incorrect")
            else:
                raise ValueError("Old password is missing in body request")
        
        user.save()
        req.context['result'] = m.User.get(id=user.id)