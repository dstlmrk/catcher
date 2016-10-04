#!/usr/bin/python
# coding=utf-8

import logging
import falcon
import smtplib
from catcher import config
from catcher.models import MySQLModel


class Login(object):

    @staticmethod
    def send_email(recipient, message):

        # TODO: nacitat z configu
        sender = 'noreply.catcher@gmail.com'

        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(
                config.email['username'],
                config.email['password']
            )
            server.sendmail(sender, recipient, message)
            server.quit()

        except Exception, ex:
            logging.error(
                "Message wasn't sended (email: %s): %s (%s)"
                % (recipient, message, ex)
            )
            falcon.HTTPInternalServerError(
                "Message wasn't sended (email: %s)" % recipient,
                "%s (%s)" % (message, ex)
            )

    @staticmethod
    def send_reset_password(user):
        ''''''
        new_password = user.generate_password()
        user.password = new_password
        user.save()

        msg = (
            "Hello,\n\n"
            "new password for your account is %s. "
            "Please change it immediately.\n\n"
            "Catcher\n\n"
            "This e-mail was generated automatically. "
            "Any reply will not be processed."
            % new_password)

        Login.send_email(user.email, msg)

    @staticmethod
    def send_init_password(user):
        ''''''
        msg = (
            "Welcome,\n\n"
            "password for your account is %s. "
            "Please change it immediately.\n\n"
            "Catcher\n\n"
            "This e-mail was generated automatically. "
            "Any reply will not be processed."
            % user.password)

        Login.send_email(user.email, msg)

    @staticmethod
    def registration(email):
        ''''''
        Login.reset_password(email)
