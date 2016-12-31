#

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
    :returns: Engine object connected with production/testing database.
    """

    test = False
    # check, if this import is called by test files
    curframe = inspect.currentframe()
    for x in inspect.getouterframes(curframe):
        if "test.py" in x[1]:
            test = True
    if not test:
        engine = create_engine(
            'mysql://{}:{}@{}/{}?charset=utf8'.format(
                config['db']['user'],
                config['db']['password'],
                config['db']['host'],
                config['db']['name']
            )
        )
        logger.debug("Connected Catcher database")
    else:
        engine = create_engine(
            'mysql://{}:{}@{}/{}?charset=utf8'.format(
                '',
                '',
                'localhost',
                'test_catcher'
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
    def beautify(value):
        if isinstance(value, int) or isinstance(value, float):
            return value
        else:
            return '\'%s\'' % value

    def __repr__(self):
        table = self.__class__.__name__
        variables = ''
        for key, value in self.__dict__.items():
            # if value is not private
            if key[:1] != '_':
                variables += '%s=%s, ' % (key, _Base.beautify(value))
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


def session(func):
    """
    It wraps all method used by rest api. Makes and closes session.
    """

    def outer_function(*args, **kwargs):
        session = Session()
        ret_val = func(*args, _session=session, **kwargs)
        session.commit()
        return ret_val

    return outer_function

Base = declarative_base(cls=_Base)
# expire_on_commit znamena, ze objekty zustanou zachovany i po commitu
Session = sessionmaker(bind=get_engine(), expire_on_commit=False)
