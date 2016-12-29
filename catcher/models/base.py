#

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

pymysql.install_as_MySQLdb()


class _Base(object):
    """
    It's made for string representation of database tables.
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
    Decorator for session commits
    """

    def outer_function(*args, **kwargs):
        session = Session()
        ret_val = func(*args, _session=session, **kwargs)
        session.commit()
        return ret_val

    return outer_function


Base = declarative_base(cls=_Base)

# echo rika, ze provadi logging
engine = create_engine('mysql://:@localhost/catcher', echo=True)
Session = sessionmaker(bind=engine)
