#!/usr/bin/python
# coding=utf-8

# import logging
# # import falcon
import peewee as pw
# # from datetime import datetime
from catcher.models import MySQLModel, CountryCode, Division

class Team(MySQLModel):

    division = pw.ForeignKeyField(Division)
    name = pw.CharField()
    shortcut = pw.CharField(max_length=3)
    city = pw.CharField()
    country = CountryCode(max_length=3)
    cald_id = pw.IntegerField()
    user_id = pw.IntegerField()

    # @classmethod
    # def select(cls, req, *selection):
    #     # note: None is as 'null' in query string
    #     possible_expressions = [
    #         cls.city == req.get_param("city"),
    #         cls.country == req.get_param("country"),
    #         cls.division == req.get_param_as_int("division_id")
    #     ]
    #     expressions = [
    #         exp for exp in possible_expressions if exp.rhs is not None
    #     ]
    #     if expressions:
    #         return super(Team, cls).select(*selection).where(*expressions)
    #     return super(Team, cls).select(*selection)

    # @classmethod
    # def create(cls, *args, **kw):
    #     ''''''
    #     cls.validate(kw['email'], kw['password'], kw['role'])
        
    #     kw['createdAt'] = str(datetime.now())
    #     kw['apiKey'] = cls.getEmptyApiKey()

    #     super(User, cls).create(*args, **kw)

    # @staticmethod
    # def login(email, password):
    #     ''''''
    #     return User.get(email=email, password=password)

    # @classmethod
    # def getEmptyApiKey(cls):
    #     ''''''
    #     for i in range(10):
    #         apiKey = uuid.uuid4().hex
    #         try:
    #             cls.get(apiKey=apiKey)
    #         except cls.DoesNotExist:
    #             return apiKey
    #         else:
    #             continue
    #     raise falcon.HTTPServiceUnavailable(
    #         "Try it again",
    #         "Catcher couldn't generate new api key, please try it again"
    #     )

    # @classmethod
    # def validate(cls, email, password, role):
    #     ''''''
    #     User.validateEmail(email)
    #     User.validatePassword(password)

    #     if role not in ["organizer"]: #, "club"]:
    #         raise falcon.HTTPBadRequest(
    #             "Bad input",
    #             "Role %s is not supported" % role
    #         )

    # @staticmethod
    # def validateEmail(email):
    #     ''''''
    #     if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    #         raise falcon.HTTPBadRequest(
    #             "Bad input",
    #             "Email format is invalid"
    #         )

    # @staticmethod
    # def validatePassword(password):
    #     ''''''
    #     if not len(password) > 5:
    #         raise falcon.HTTPBadRequest(
    #             "Bad input",
    #             "Password is too much short"
    #         )

    # def substituteEmail(self, email):
    #     ''''''
    #     if email:
    #         self.validateEmail(email)
    #         self.email = email

    # def substitutePassword(self, password, newPassword):
    #     ''''''
    #     if password and newPassword:
    #         verifyPassword(password)
    #         User.validatePassword(newPassword)
    #         self.password = newPassword

    # def verifyPassword(self, password):
    #     '''Pripraveno pro prevod z hashe do realu'''
    #     if self.password == password:
    #         return True
    #     else:
    #         raise falcon.HTTPBadRequest(
    #             "Bad input", "Password is incorrect"
    #         )
