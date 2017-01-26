from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.exc import IntegrityError
from catcher.models.base import Base
from catcher.models import Role, Email, ApiKey
from sqlalchemy.orm import relationship, joinedload, contains_eager
import re
import random
import string
import time


class NullUser(object):
    """Represents anonymous user"""

    class Role(object):
        type = None
        id = None

    id = None
    login = None
    role = Role()


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
    def create(session, login, email, password, role_id):
        """Create new user"""
        user = User(
            login=login,
            email=User._validate_email(email),
            password=User._validate_password(password),
            role_id=role_id
        )
        session.add(user)
        session.flush()
        return user

    @staticmethod
    def register(session, login, email):
        """
        Checks valid email, generates init password and sends email.
        This method is available for create of users (no admins) only.
        Result of registration is new user with user role (no admin).
        """
        role = session.query(Role).filter(Role.type == "user").one()
        try:
            user = User.create(
                session, login, email, User._generate_password(), role.id
            )
        except IntegrityError:
            raise ValueError("User already exists with this login or email")
        Email.registration(user)
        return user

    def to_dict(self):
        dictionary = super(User, self).to_dict()
        del dictionary['password']
        return dictionary

    @staticmethod
    def get(session, id):
        """Get user by id"""
        return session.query(User).get(id)

    @staticmethod
    def get_by_auth(session, auth):
        """Get user by authorization token."""
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
    def get_all(session, **kwargs):
        """Get all users"""
        return [
            user for user in session.query(User)\
                                    .options(joinedload('role'))\
                                    .filter_by(**kwargs)
        ]

    @staticmethod
    def edit(session, id, login=None, email=None, password=None, role_id=None):
        """Edit user"""
        user = session.query(User).get(id)
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
    def delete(session, id):
        """Delete user"""
        return session.query(User).filter(User.id == id).delete()

    @staticmethod
    def get_by_credentials(session, login, password):
        return session.query(User) \
            .options(joinedload('role')) \
            .filter_by(login=login, password=password) \
            .one()

    @staticmethod
    def log_in(session, login, password):
        """
        :returns: user, token and its validity.
        """
        user = User.get_by_credentials(session, login, password)
        # TODO: vracet jenom objekt user obohaceny o token s platnosti
        api_key, validity = ApiKey.create(session, user)
        return user, api_key, validity

    @staticmethod
    def _generate_password():
        """Generate random password"""
        return ''.join(
            random.choice(
                string.ascii_uppercase + string.digits
            ) for x in range(8)
        )

    @staticmethod
    def _validate_login(login):
        """Check login if his minimal length is six"""
        if len(login) < 6:
            raise ValueError(
                'Login is too much short.'
                ' It has to have minimal 6 characters.'
            )
        return login

    @staticmethod
    def _validate_email(email):
        """Check email if its format is valid"""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Email format is invalid')
        return email

    @staticmethod
    def _validate_password(password):
        """Check password if his minimal length is six"""
        if len(password) < 6:
            raise ValueError(
                'Password is too much short.'
                ' It has to have minimal 6 characters.'
            )
        return password
