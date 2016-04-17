#!/usr/bin/python
# coding=utf-8

from catcher import models as m
from catcher.api.privileges import *
import falcon

class Login(object):

    def on_post(self, req, resp):
        '''check login'''
        try:
            req.context['result'] = m.User.login(**req.context['data'])
        except:
            raise falcon.HTTPUnauthorized(
                "Authentication Failed",
                "Email or password is wrong."
            )

class ForgottenPassword(object):

    @falcon.before(Privilege("admin"))
    def on_post(self, req, resp):
        '''send new password'''
        pass


# TODO: napsat tridu pro obnoveni hesla (poslat email s novym heslem asi)

# PERFMORMIO -------------------------

# class ForgottenPassword(Resource):
#     MEM_KEY = "forgottenPassword_%s"
#     EXPIRE = 600

#     def on_post(self, req, resp):
#         """
#         odesle email s odkazem pro zmenu hesla
#         """
#         req.context['result'] = {}
#         user = models.AdminUser.byEmail(req.context['data']['email'])
#         hash = uuid.uuid4().hex
#         assert config.memcache.set(self.MEM_KEY % hash, user.id, self.EXPIRE)
#         notification.sendResetPassword(user, hash, req)

# class ResetPassword(Resource):
#     def on_post(self, req, resp):
#         """
#         nastavi nove heslo
#         """
#         memcache = config.memcache
#         key = ForgottenPassword.MEM_KEY % req.context['data']['hash']
#         userId = memcache.get(key)
#         if not userId:
#             raise falcon.HTTPForbidden(
#                 "Forbidden",
#                 "Reset password hash is invalid"
#             )
#         memcache.delete(key)
#         user = models.AdminUser.get(userId)
#         user.password = req.context['data']['password']

# import hashlib

# class AdminUser(SQLModel):
#     class sqlmeta:
#         fromDatabase = True

#     apiKey = StringCol(unique=True, default=lambda: uuid.uuid4().get_hex())
#     salt = "J2e$w^b!j(k_v"
#     agencies = RelatedJoin("Agency", intermediateTable="agency_has_admin_user")
#     campaigns = RelatedJoin("Campaign", intermediateTable="campaign_has_admin_user")
#     clients = RelatedJoin("Client", intermediateTable="client_has_admin_user")


#     def _getPasswordHash(self, email, password):
#         return hashlib.sha256("%s:%s:%s" % (email, password, AdminUser.salt)).hexdigest()

#     @staticmethod
#     def login(email, password):
#         return AdminUser.selectBy(
#             email = email,
#             password = password,
#             deleted = 0
#         ).getOne()

#     def set_password(self, value):
#         return self._getPasswordHash(self.email, value)