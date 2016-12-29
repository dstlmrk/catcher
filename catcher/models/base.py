#

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

pymysql.install_as_MySQLdb()

Base = declarative_base()

# echo rika, ze provadi logging
engine = create_engine('mysql://:@localhost/catcher', echo=True)
Session = sessionmaker(bind=engine)


def session(func):
    """Decorator for session commits"""

    def outer_function(*args, **kwargs):
        session = Session()
        ret_val = func(*args, _session=session, **kwargs)
        session.commit()
        return ret_val

    return outer_function
