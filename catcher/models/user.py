#!/usr/bin/python
# coding=utf-8

import falcon
import uuid
import re
import peewee as pw
from catcher.models import MySQLModel


class Role(MySQLModel):
    role = pw.CharField()


class User(MySQLModel):

    email = pw.CharField()
    password = pw.CharField()
    created_at = pw.DateTimeField(db_column='created_at')
    api_key = pw.CharField(db_column='api_key')
    role = pw.ForeignKeyField(Role)

    @classmethod
    def create(cls, *args, **kw):
        '''Creates new user and validates input data'''
        cls.validate(kw['email'], kw['password'], kw['role'])
        kw['api_key'] = cls.getEmptyApiKey()
        kw['role'] = Role.get(role=kw['role']).id
        return super(User, cls).create(*args, **kw)

    @staticmethod
    def login(email, password):
        ''''''
        user = User.get(email=email, password=password)

        return user

    @classmethod
    def getEmptyApiKey(cls):
        ''''''
        for i in range(10):
            api_key = uuid.uuid4().hex
            try:
                cls.get(api_key=api_key)
            except cls.DoesNotExist:
                return api_key
            else:
                continue
        raise falcon.HTTPServiceUnavailable(
            "Try it again",
            "Catcher couldn't generate new api key, please try it again"
        )

    @classmethod
    def validate(cls, email, password, role):
        ''''''
        User.validateEmail(email)
        User.validatePassword(password)

        if role not in ["organizer"]:
            raise falcon.HTTPBadRequest(
                "Bad input",
                "Role %s is not supported" % role
            )

    @staticmethod
    def validateEmail(email):
        ''''''
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise falcon.HTTPBadRequest(
                "Bad input",
                "Email format is invalid"
            )

    @staticmethod
    def validatePassword(password):
        ''''''
        if not len(password) > 5:
            raise falcon.HTTPBadRequest(
                "Bad input",
                "Password is too much short"
            )

    def substituteEmail(self, email):
        ''''''
        if email:
            self.validateEmail(email)
            self.email = email

    def substitutePassword(self, password, newPassword):
        ''''''
        if password and newPassword:
            self.verifyPassword(password)
            User.validatePassword(newPassword)
            self.password = newPassword

    def verifyPassword(self, password):
        '''Pripraveno pro prevod z hashe do realu'''
        if self.password == password:
            return True
        else:
            raise falcon.HTTPBadRequest(
                "Bad input", "Password is incorrect"
            )


class NullUser(object):

    class Role(object):
        pass

    role = Role()
    role.role = None
    api_key = None
