#

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm.exc import NoResultFound
from catcher.models.base import Base, session
from catcher.models import Role, Email, ApiKey
import re
import random
import string
import time


class NullUser():
    """Represents anonymous user."""
    role_id = None
    api_key = None


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=time.strftime('%Y-%m-%d %H:%M:%S'))
    role_id = Column(Integer, ForeignKey('role.id'))

    def __repr__(self):
        return "<User(id='%s', email='%s', password='%s', created_at='%s', role_id='%s')>" % (
            self.id, self.email, self.password, self.created_at, self.role_id)

    @staticmethod
    @session
    def create(email, role, _session):
        """
        POST /users
        It checks valid email, generates init password and sends email.
        """

        User._validate_email(email)
        # TODO: vratit zpet na generovani nahodneho hesla
        # init_password = User._generate_password()
        init_password = 'heslo'

        role_id = _session.query(Role).filter(Role.type == role).one().id
        user = User(email=email, password=init_password, role_id=role_id)
        Email.registration(user)
        _session.add(user)

    @staticmethod
    @session
    def login(email, password, _session):
        """
        POST /login
        :returns: Api key and its validity.
        """
        try:
            user = _session.query(User).filter_by(email=email, password=password).one()
        except NoResultFound:
            raise ValueError("Authentication Failed: email or password is wrong")
        return ApiKey.create(user, _session)

    @staticmethod
    @session
    def logout(api_key, _session):
        """
        POST /logout
        """
        _session.query(ApiKey).filter(ApiKey.key == api_key).delete()

    @staticmethod
    def get_user(email, password):
        # TODO: chci vracet uzivatele pro middleware (nejsem si jisty, zda je to potreba)
        return None

    @staticmethod
    def _generate_password():
        """
        :return: Random password.
        """
        return ''.join(
            random.choice(
                string.ascii_uppercase + string.digits
            ) for x in range(8)
        )

    @staticmethod
    def _validate_email(email):
        """"""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email format is invalid")


    # def substituteEmail(self, email):
    #     ''''''
    #     if email:
    #         self.validateEmail(email)
    #         self.email = email
    #
    # def substitutePassword(self, password, newPassword):
    #     ''''''
    #     if password and newPassword:
    #         self.verifyPassword(password)
    #         User.validatePassword(newPassword)
    #         self.password = newPassword
    #
    # def verifyPassword(self, password):
    #     '''Pripraveno pro prevod z hashe do realu'''
    #     if self.password == password:
    #         return True
    #     else:
    #         raise falcon.HTTPBadRequest(
    #             "Bad input", "Password is incorrect"
    #         )
