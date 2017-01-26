import smtplib
from catcher.config import config
from catcher.logger import logger


class Email(object):

    @staticmethod
    def _send_email(recipient, message):
        """Send email"""
        sender = config['email']['username']
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(sender, config['email']['password'])
            server.sendmail(sender, recipient, message)
            server.quit()
        except Exception as ex:
            logger.error("Email sending to %s finished with error %s" % (recipient, ex.__traceback__))
            raise Exception("Email sending finished with error")
        logger.warn("Email is sent in %s" % recipient)

    # TODO: check method for reset_password
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

    @staticmethod
    def registration(user):
        """Create message for new user and send it"""
        msg = (
            "Welcome,\n\n"
            "password for your account is %s. "
            "Please change it immediately.\n\n"
            "Catcher\n\n"
            "This e-mail was generated automatically. "
            "Any reply will not be processed.\n"
            % user.password)
        Email._send_email(user.email, msg)
