#

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm.exc import NoResultFound
from catcher.models.base import Base, session
from catcher.models import Role, Email, ApiKey
from sqlalchemy.orm import relationship
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
    login = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=time.strftime('%Y-%m-%d %H:%M:%S'))
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship("Role")

    @staticmethod
    @session
    def create(login, email, role, _session):
        """
        POST /users
        It checks valid email, generates init password and sends email.
        """
        # TODO: vratit zpet na generovani nahodneho hesla
        # init_password = User._generate_password()
        init_password = 'heslo'
        role_id = _session.query(Role).filter(Role.type == role).one().id
        user = User(
            login=login,
            email=User._validate_email(email),
            password=init_password,
            role_id=role_id
        )
        Email.registration(user)
        _session.add(user)
        return user

    def to_dict(self):
        dictionary = super(User, self).to_dict()
        del dictionary['password']
        del dictionary['role_id']
        # ineffective: makes another select which saves in the cache
        dictionary['role'] = self.role.type
        return dictionary

    @staticmethod
    @session
    def get(id, _session):
        """
        GET /user/{id}
        """
        return _session.query(User).filter(User.id == id).one()

    @staticmethod
    @session
    def get_users(_session, **kwargs):
        # TODO: join s rolemi a jejim nazvem, nechci vracet id
        return [user for user in _session.query(User).filter_by(**kwargs)]

    @staticmethod
    @session
    def edit(id, _session, email=None, password=None):
        user = _session.query(User).get(id)
        if email:
            user.email = User._validate_email(email)
        if password:
            user.password = User._validate_password(password)
        return user

    @staticmethod
    @session
    def log_in(login, password, _session):
        """
        POST /login
        :returns: Api key and its validity.
        """
        try:
            user = _session.query(User).filter_by(login=login, password=password).one()
        except NoResultFound:
            raise ValueError("Authentication Failed: email or password is wrong")
        return ApiKey.create(user, _session)

    @staticmethod
    @session
    def log_out(api_key, _session):
        """
        POST /logout
        """
        _session.query(ApiKey).filter(ApiKey.key == api_key).delete()

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
            raise ValueError('Email format is invalid')
        return email

    @staticmethod
    def _validate_password(password):
        """"""
        if not len(password) > 5:
            raise ValueError(
                'Password is too much short. It have to minimal 5 characters.'
            )
        return password
