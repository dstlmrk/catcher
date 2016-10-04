# #!/usr/bin/python
# # coding=utf-8

# import logging
# import falcon
# import uuid
# import re
# import string
# import smtplib
# import peewee as pw
# from datetime import datetime
# from catcher.models import MySQLModel

# class User(MySQLModel):

#     email = pw.CharField()
#     password = pw.CharField()
#     createdAt = pw.DateTimeField(db_column='created_at')
#     apiKey = pw.CharField(db_column='api_key')
#     role = pw.CharField()
#     clubId = pw.IntegerField(db_column='club_id')

#     @classmethod
#     def create(cls, *args, **kw):
#         ''''''
#         cls.validate(kw['email'], kw['password'], kw['role'])
        
#         kw['createdAt'] = str(datetime.now())
#         kw['apiKey'] = cls.getEmptyApiKey()

#         super(User, cls).create(*args, **kw)

#     @staticmethod
#     def login(email, password):
#         ''''''
#         return User.get(email=email, password=password)

#     @classmethod
#     def getEmptyApiKey(cls):
#         ''''''
#         for i in range(10):
#             apiKey = uuid.uuid4().hex
#             try:
#                 cls.get(apiKey=apiKey)
#             except cls.DoesNotExist:
#                 return apiKey
#             else:
#                 continue
#         raise falcon.HTTPServiceUnavailable(
#             "Try it again",
#             "Catcher couldn't generate new api key, please try it again"
#         )

#     @classmethod
#     def validate(cls, email, password, role):
#         ''''''
#         User.validateEmail(email)
#         User.validatePassword(password)

#         if role not in ["organizer"]: #, "club"]:
#             raise falcon.HTTPBadRequest(
#                 "Bad input",
#                 "Role %s is not supported" % role
#             )

#     @staticmethod
#     def validateEmail(email):
#         ''''''
#         if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
#             raise falcon.HTTPBadRequest(
#                 "Bad input",
#                 "Email format is invalid"
#             )

#     @staticmethod
#     def validatePassword(password):
#         ''''''
#         if not len(password) > 5:
#             raise falcon.HTTPBadRequest(
#                 "Bad input",
#                 "Password is too much short"
#             )

#     def substituteEmail(self, email):
#         ''''''
#         if email:
#             self.validateEmail(email)
#             self.email = email

#     def substitutePassword(self, password, newPassword):
#         ''''''
#         if password and newPassword:
#             verifyPassword(password)
#             User.validatePassword(newPassword)
#             self.password = newPassword

#     def verifyPassword(self, password):
#         '''Pripraveno pro prevod z hashe do realu'''
#         if self.password == password:
#             return True
#         else:
#             raise falcon.HTTPBadRequest(
#                 "Bad input", "Password is incorrect"
#             )
