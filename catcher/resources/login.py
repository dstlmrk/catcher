#!/usr/bin/python
# coding=utf-8

from catcher import models as m
from catcher.api.privileges import *
import falcon
import smtplib
import random
import string
import logging
from catcher import config

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

    def on_post(self, req, resp):
        '''send new password'''
        email = req.params['email']
        print email
        try:
            user = m.User.get(email=email)
        except m.User.DoesNotExist:
            raise ValueError("User with email %s doesn't exist" % email)

        newPassword = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for x in range(8)
            )
        
        msg = ("Hello,\n\nnew password for your account is %s. Please change it immediately.\n\n"
            "Catcher\n\nThis e-mail was generated automatically. Any reply will not be processed."
            % newPassword)

        fromAddr = 'noreply.catcher@gmail.com'
        toAddrs  = email

        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(config.email['username'], config.email['password'])
            server.sendmail(fromAddr, toAddrs, msg)
            server.quit()
            user.password = newPassword
            user.save()
        except Exception, ex:
            logging.error("Reset password for %s wasn't successful (%s)" % (email,ex))
            falcon.HTTPInternalServerError(title, description, **kwargs)