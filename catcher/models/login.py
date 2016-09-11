#!/usr/bin/python
# coding=utf-8

import logging
import falcon
import smtplib
import random
import string
from catcher import config
from catcher.models import MySQLModel

class Login(object):

    @staticmethod
    def sendEmail(email, message):

        # TODO: nacitat z configu
        fromEmail = 'noreply.catcher@gmail.com'
        toEmail = email

        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(
                config.email['username'],
                config.email['password']
            )
            server.sendmail(fromEmail, toEmail, msg)
            server.quit()
            user.password = newPassword
            user.save()

        except Exception, ex:
            logging.error(
                "Message wasn't sended (email: %s): %s (%s)"
                % (email, message, ex)
            )
            falcon.HTTPInternalServerError(
                "Message wasn't sended (email: %s)" % email,
                "%s (%s)" % (message, ex),
                **kwargs
            )

    @staticmethod
    def generatePassword():
        '''
        Generates new random password
        '''
        return ''.join(
            random.choice(
                string.ascii_uppercase + string.digits
            ) for x in range(8)
        )

    @staticmethod
    def resetPassword(user):
        ''''''
        newPassword = Login.generatePassword()
        user.password = newPassword
        user.save()

        msg = (
            "Hello,\n\n"
            "new password for your account is %s. "
            "Please change it immediately.\n\n"
            "Catcher\n\n"
            "This e-mail was generated automatically. "
            "Any reply will not be processed."
            % newPassword)

        Login.sendEmail(user.email, msg)

    @staticmethod
    def registration(email):
        ''''''
        Login.resetPassword(email)