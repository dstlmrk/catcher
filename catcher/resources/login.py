from catcher import models
from falcon import HTTPUnauthorized, HTTP_201
from catcher.logger import logger


class Login():

    def on_post(self, req, resp):
        """Check login and password and return random api key"""
        try:
            user, api_key, validity = models.User.log_in(
                **req.context['data']
            )
        except:
            raise HTTPUnauthorized(
                "Authentication Failed",
                "Login or password is wrong.",
                ""
            )
        # TODO: potrebuje klient platnost, kdyz je neustale prodluzovana?
        req.context['result'] = {
            "user": user,
            "api_key": api_key,
            "validity": validity
        }
        resp.status = HTTP_201


class Registration():

    def on_post(self, req, resp):
        """Register new user with basic role and send email him"""
        models.User.register(**req.context['data'])
        resp.status = HTTP_201


class ResetPassword():

    def on_post(self, req, resp):
        """Send password on user's email"""
        user_email = req.context['data']['email']
        logger.error(
            "%s calls /api/reset-password that isn't implemented" % user_email
        )
        raise NotImplementedError
