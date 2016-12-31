#!/usr/bin/python
# coding=utf-8

import smtplib
from catcher.config import config


class Email():

    @staticmethod
    def _send_email(recipient, message):

        # TODO: potreba otestovat pousteni emailu

        # TODO: load from config file
        sender = 'noreply.catcher@gmail.com'

        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(
                config['email']['username'],
                config['email']['password']
            )
            server.sendmail(sender, recipient, message)
            server.quit()

        except Exception as ex:
            # TODO: doladit vyhazovani vyjimek a posilani zprav do logovani
            raise Exception("Email error")
            # logging.error(
            #     "Message wasn't sended (email: %s): %s (%s)"
            #     % (recipient, message, ex)
            # )
            # falcon.HTTPInternalServerError(
            #     "Message wasn't sended (email: %s)" % recipient,
            #     "%s (%s)" % (message, ex)
            # )

    # @staticmethod
    # def send_reset_password(user):
    #     ''''''
    #     new_password = user.generate_password()
    #     user.password = new_password
    #     user.save()
    #
    #     msg = (
    #         "Hello,\n\n"
    #         "new password for your account is %s. "
    #         "Please change it immediately.\n\n"
    #         "Catcher\n\n"
    #         "This e-mail was generated automatically. "
    #         "Any reply will not be processed."
    #         % new_password)
    #
    #     Login.send_email(user.email, msg)
    #


    @staticmethod
    def registration(user):
        ''''''
        msg = (
            "Welcome,\n\n"
            "password for your account is %s. "
            "Please change it immediately.\n\n"
            "Catcher\n\n"
            "This e-mail was generated automatically. "
            "Any reply will not be processed."
            % user.password)
        # TODO: dokoncit odeslani
        # Email._send_email(user.email, msg)
