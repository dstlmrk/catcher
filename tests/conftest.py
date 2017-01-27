import os
import sys
# Ondra's tip for _pytest.config.ConftestImportFailure: ImportMismatchError('conftest', ...
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, ROOT_DIR)

import pytest
from catcher.config import config
from catcher.logger import logger
from catcher.models import User, Team
from catcher.models.base import Session
from db.database import Database

logger.setLevel('DEBUG')


@pytest.yield_fixture(scope='session')
def database_maker():
    """
    Creates test database by original and after tests it deletes it.
    """
    db = Database(config['db']['name'], 'localhost', '', '')
    db.dump()
    db.create()
    yield db
    # it is not used because on the travis is not database
    # and I need dump available for later
    # db.remove_temp_files()
    db.delete()


@pytest.yield_fixture(scope='function')
def database(database_maker):
    """
    Fills database before each test and gives session.
    """
    database_maker.fill()
    yield None
    database_maker.clean()
    database_maker.conn.commit()


@pytest.yield_fixture(scope='function')
def session(database):
    """
    Fills database before each test and gives session.
    """
    session = Session()
    yield session
    session.close()


@pytest.fixture(scope='function')
def users(session):
    session.add(User(
        id=1, login="user1", email="user1@test.cz",
        password="password1", role_id=1
    ))
    session.add(User(
        id=2, login="user2", email="user2@test.cz",
        password="password2", role_id=1
    ))
    # admin
    session.add(User(
        id=3, login="admin_login", email="user3@test.cz",
        password="admin_password", role_id=2
    ))
    session.commit()


@pytest.fixture(scope='function')
def teams(session):
    session.add(Team(
        id=1, division_id=1, name="FC Prague", shortcut="FCP",
        city="Prague", country="CZE"
    ))
    session.add(Team(
        id=2, division_id=2, name="FC Hradec Králové", shortcut="HK",
        city="Hradec Králové", country="CZE"
    ))
    session.commit()
