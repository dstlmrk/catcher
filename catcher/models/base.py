#

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.types as types
from iso3166 import countries

pymysql.install_as_MySQLdb()


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

# echo rika, ze provadi logging
engine = create_engine('mysql://:@localhost/catcher?charset=utf8', echo=True)
Session = sessionmaker(bind=engine)
