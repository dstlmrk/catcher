import pymysql
import inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.types as types
from iso3166 import countries
from catcher.config import config
from catcher.logger import logger
pymysql.install_as_MySQLdb()


def get_engine():
    """
    Return engine object connected with production/testing database.
    Engine supports connection pool by default. Its size is 5.
    """
    test = False
    database_url = 'mysql://{}:{}@{}/{}?charset=utf8'

    # check, if this import is called by test files
    cur_frame = inspect.currentframe()
    for x in inspect.getouterframes(cur_frame):
        if 'conftest.py' in x[1]:
            test = True

    if not test:
        engine = create_engine(database_url.format(
                config['db']['user'],
                config['db']['password'],
                config['db']['host'],
                config['db']['name']
            )
        )
        logger.info("Connected Catcher database")
    else:
        engine = create_engine(database_url.format(
                '', '', 'localhost', 'test_catcher'
            )
        )
        logger.warn("Connected test database")
    return engine


class CountryCode(types.UserDefinedType):
    """
    Custom column checks if field is country by ISO 3166-1 alpha-3
    """

    def get_col_spec(self):
        return "COUNTRYCODE(%s)" % self.length

    def bind_processor(self, dialect):
        def process(value):
            if not value:
                return value
            try:
                countries.get(value)
            except KeyError:
                raise ValueError('Country by ISO 3166-1 alpha-3 not found')
            return value
        return process


class _Base(object):
    """
    Made for string representation of database tables.
    """

    @staticmethod
    def _beautify(value):
        if isinstance(value, int) or isinstance(value, float):
            return value
        else:
            return '\'%s\'' % value

    @staticmethod
    def _is_public(key):
        return key[:1] != '_'

    def __repr__(self):
        table = self.__class__.__name__
        variables = ''
        for key, value in self.__dict__.items():
            # if value is not private
            if _Base._is_public(key):
                variables += '%s=%s, ' % (key, _Base._beautify(value))
        variables = variables[:-2]
        return '<%s(%s)>' % (table, variables)

    # for testing
    def __eq__(self, other):
        """Override the default Equals behavior"""
        if type(other) is type(self):
            return self.__repr__() == other.__repr__()
        return NotImplemented

    # for testing
    def __ne__(self, other):
        """Define a non-equality test"""
        if type(other) is type(self):
            return not self.__eq__(other)
        return NotImplemented

    def to_dict(self):
        # TODO: returns attributes only, but I want methods also (e.g. relationship)
        dictionary = {}
        for key, value in self.__dict__.items():
            if _Base._is_public(key):
                dictionary[key] = value
        return dictionary


def session(func):
    """
    It wraps all method used by rest api. Makes and closes session.
    """

    def outer_function(*args, **kwargs):
        session = get_session()
        ret_val = func(*args, _session=session, **kwargs)
        # returns the connection to the pool
        session.commit()
        return ret_val

    return outer_function


def get_session():
    return Session()

Base = declarative_base(cls=_Base)
# expire_on_commit znamena, ze objekty zustanou zachovany i po commitu
Session = sessionmaker(bind=get_engine(), expire_on_commit=False)
