from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import  IntegrityError
from catcher.models.base import Base, session
from catcher.models import Role, Email, ApiKey
from sqlalchemy.orm import relationship, joinedload, contains_eager
import re
import random
import string
import time

from catcher.logger import logger


class NullUser():
    """Represents anonymous user"""

    class Role():
        type = None
        id = None

    id = None
    login = None
    role = Role()
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

    # TODO: admin ma moznost vytvorit uzivatele manualne
    # TODO: bezne se ale uzivatel registruje pres metodu register, protoze ta posila heslo (vyuzit dedicnost nebo skladani metod!!!!!!!, abych nemel duplicitni kod)
    @staticmethod
    @session
    def create(login, email, role_id, _session):
        """
        POST /users
        It checks valid email, generates init password and sends email.
        """
        # TODO: vratit zpet na generovani nahodneho hesla
        # init_password = User._generate_password()
        init_password = 'heslo'
        # role_id = _session.query(Role).filter(Role.type == role).one().id
        user = User(
            login=login,
            email=User._validate_email(email),
            password=init_password,
            role_id=role_id
        )
        _session.add(user)
        return user

    @staticmethod
    @session
    def register(login, email, _session):
        """
        Checks valid email, generates init password and sends email.
        This method is available for create of users (no admins) only.
        Result of registration is new user with user role (no admin).
        """
        # result of registration is new user (no admin)
        role = _session.query(Role).filter(Role.type == "user").one()
        user = User(
            login=login,
            email=User._validate_email(email),
            password=User._generate_password(),
            role_id=role.id
        )
        _session.add(user)
        try:
            _session.commit()
        except IntegrityError:
            raise ValueError("User already exists with this login or email")
        Email.registration(user)
        return user

    def to_dict(self):
        dictionary = super(User, self).to_dict()
        del dictionary['password']
        # del dictionary['role_id']
        # ineffective: makes another select which saves in the cache
        # dictionary['role'] = self.role.type
        return dictionary

    @staticmethod
    @session
    def get(id, _session):
        """
        GET /user/{id}
        """
        return _session.query(User).get(id)
        # return _session.query(User).filter(User.id == id).one()

    @staticmethod
    def get_by_auth(auth, session):
        """
        Get user by authorization token. It uses by middleware.
        """
        api_key = (session.query(ApiKey)
                          .join(User)
                          .join(Role)
                          .options(
                              contains_eager(ApiKey.user).
                              contains_eager(User.role))
                          .filter(ApiKey.key == auth)
                   ).one()
        return api_key.user

    @staticmethod
    @session
    def get_all(_session, **kwargs):
        return [user for user in _session.query(User).options(joinedload('role')).filter_by(**kwargs)]

    @staticmethod
    @session
    # TODO: pridat opravneni, aby heslo mohl menit pouze admin nebo sam uzivatel
    # TODO: login, role_id muze menit jenom admin
    def edit(id, _session, login=None, email=None, password=None, role_id=None):
        user = _session.query(User).get(id)
        if login:
            user.login = login
        if email:
            user.email = User._validate_email(email)
        if password:
            user.password = User._validate_password(password)
        if role_id:
            user.role_id = role_id
        return user

    @staticmethod
    @session
    def delete(id, _session):
        return _session.query(User).filter(User.id == id).delete()

    @staticmethod
    @session
    def log_in(login, password, _session):
        """
        POST /login
        :returns: Api key and its validity.
        """
        try:
            user = _session.query(User).options(joinedload('role')).filter_by(login=login, password=password).one()
        except NoResultFound:
            logger.warn("NoResultFound")
            raise ValueError("Authentication Failed: login or password is wrong")
        return (user, ApiKey.create(user, _session))

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
    def _validate_login(login):
        """"""
        if len(login) < 6:
            raise ValueError(
                'Login is too much short. It has to have minimal 6 characters.'
            )
        return login

    @staticmethod
    def _validate_email(email):
        """"""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Email format is invalid')
        return email

    @staticmethod
    def _validate_password(password):
        """"""
        if len(password) < 6:
            raise ValueError(
                'Password is too much short. It has to have minimal 6 characters.'
            )
        return password
