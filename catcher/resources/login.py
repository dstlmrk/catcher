from catcher import models
from falcon import HTTPUnauthorized

class Login():

    def on_post(self, req, resp):
        """
        Checks login
        """
        try:
            req.context['result'] = models.User.login(**req.context['data'])
        except:
            raise HTTPUnauthorized(
                "Authentication Failed",
                "Email or password is wrong.",
                ""
            )

class Registration():

    def on_post(self, req, resp):
        """"""
        print("registration")

class ResetPassword():

    def on_post(self, req, resp):
        """"""
        print("reset password")

# # pracovni zdrojak
# class ForgottenPassword(Resource):
# 	MEM_KEY = "forgottenPassword_%s"
# 	EXPIRE = 600
#
# 	def on_post(self, req, resp):
# 		"""
# 		odesle email s odkazem pro zmenu hesla
# 		"""
# 		req.context['result'] = {}
# 		user = models.AdminUser.byEmail(req.context['data']['email'])
# 		hash = uuid.uuid4().hex
# 		assert config.memcache.set(self.MEM_KEY % hash, user.id, self.EXPIRE)
# 		notification.sendResetPassword(user, hash, req)
#
# class ResetPassword(Resource):
# 	def on_post(self, req, resp):
# 		"""
# 		nastavi nove heslo
# 		"""
# 		memcache = config.memcache
# 		key = ForgottenPassword.MEM_KEY % req.context['data']['hash']
# 		userId = memcache.get(key)
# 		if not userId:
# 			raise falcon.HTTPForbidden(
# 				"Forbidden",
# 				"Reset password hash is invalid"
# 			)
# 		memcache.delete(key)
# 		user = models.AdminUser.get(userId)
# 		user.password = req.context['data']['password']
#
# # muj zdrojak
# class ForgottenPassword(object):
#
#     def on_post(self, req, resp):
#         '''send new password'''
#         email = req.params['email']
#         try:
#             user = models.User.get(email=email)
#         except User.DoesNotExist:
#             # TODO: mel bych vracet OK, protoze potvrzeni chodi na email
#             raise falcon.HTTPBadRequest(
#                 "Bad input",
#                 "User with email %s doesn't exist" % email
#             )
#         models.Login.send_reset_password(user)
