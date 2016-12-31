# #!/usr/bin/python
# # coding=utf-8

import pymysql
import pytest
from sqlalchemy import create_engine

from sqlalchemy import insert

from sqlalchemy.orm import sessionmaker
from tests.database import Database
from tests.models import *

from catcher.models import User, Team
from catcher.config import config
from catcher.logger import logger
logger.setLevel('DEBUG')

engine = create_engine(
    'mysql://:@localhost/test_catcher?charset=utf8'
)
Session = sessionmaker(bind=engine, expire_on_commit=False)

@pytest.yield_fixture(scope='session')
def database():
    """
    Creates test database by original and after tests it deletes it.
    """

    database = Database(
        config['db']['name'], 'localhost', '', ''
    )
    database.dump()
    database.create()
    yield database
    database.remove_temp_files()
    # database.delete()


@pytest.yield_fixture(scope='function')
def session(database):
    """
    Fills database before each test and gives session.
    """
    database.fill()
    session = Session()
    yield session
    database.clean()
    database.conn.commit()


# @pytest.fixture
# def app(db):
#     '''It uses for falcon testing'''
#     restapi.api.req_options.auto_parse_form_urlencoded = True
#     return restapi.api


# @pytest.fixture
# def models(db):
#     return True
#     return catcher_models


# def users():
#     pass

@pytest.fixture(scope='function')
def users(session):
    session.add(User(
        id=1, login="user1", email="user1@test.cz", password="password1", role_id=1
    ))
    session.add(User(
        id=2, login="user2", email="user2@test.cz", password="password2", role_id=1
    ))
    # admin
    session.add(User(
        id=3, login="user3", email="user3@test.cz", password="password3", role_id=2
    ))
    session.commit()


@pytest.fixture(scope='function')
def teams(session):
    # id, division_id, name, shortcut, city, country, cald_id, user_id
    session.add(Team(
        id=1, division_id=1, name="FC Prague", shortcut="FCP",
        city="Prague", country="CZE"
    ))
    session.add(Team(
        id=2, division_id=2, name="FC Hradec Králové", shortcut="HK",
        city="Hradec Králové", country="CZE"
    ))
    session.commit()
