import smtplib
from catcher.config import config
from catcher.logger import logger


class Email():

    @staticmethod
    def _send_email(recipient, message):
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
            logger.error("Email sending to %s finished with error %s" % (recipient, ex.__traceback__))
            # TODO: obyc exception by se mela zachytit falconem a pretvorit na internal server error
            raise Exception("Email sending finished with error")
        logger.debug("Email is sent in %s" % recipient)

    # TODO: zkontrolovat metodu pro obnovu hesla
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
        ''''''
        msg = (
            "Welcome,\n\n"
            "password for your account is %s. "
            "Please change it immediately.\n\n"
            "Catcher\n\n"
            "This e-mail was generated automatically. "
            "Any reply will not be processed."
            % user.password)
        # TODO: staci odkomentovat a budu posilat emaily
        logger.warn("Email is sent.. jenom jako")
        # Email._send_email(user.email, msg)
