#!/usr/bin/python
# coding=utf-8

from catcher import logger
from catcher import models as catcher_models
from catcher import config
from catcher import restapi
from catcher.test.database import Database
import pytest
from tests import *


@pytest.yield_fixture(scope='session')
def database():
    database = Database(
        config.db['name'],
        config.db['host'],
        config.db['user'],
        config.db['passwd'],
        catcher_models.db
    )
    database.dump()
    database.create()
    yield database
    database.remove_temp_files()
    database.delete()


@pytest.yield_fixture(scope='function')
def db(database):
    database.fill()
    yield True
    database.clean()


@pytest.fixture
def app(db):
    '''It uses for falcon testing'''
    restapi.api.req_options.auto_parse_form_urlencoded = True
    return restapi.api


@pytest.fixture
def models(db):
    return catcher_models


@pytest.fixture(scope='function')
def users(models):
    models.User.create(
        id=1,
        email='mickey@mouse.com',
        password="e8WFffXew",
        role="organizer"
    )
    models.User.create(
        id=2,
        email='adam@mouse.com',
        password="T3Cfp9HYt",
        role="organizer"
    )
    models.User.insert(
        id=3,
        email='admin@catcher.cz',
        password="Rf3;c9HYt",
        role=2, # admin
        api_key="#apiKeyAdmin"
    ).execute()


@pytest.fixture(scope='function')
def teams(models, users):
    models.Team.insert(
        id=1, division=1, name="Frozen Angels", shortcut="FAL",
        city="Liberec", country="CZE", user_id=1,
    ).execute()
    models.Team.insert(
        id=2, division=2, name="KeFEAR", shortcut="KEF",
        city="Košice", country="SVK", user_id=2,
    ).execute()
    models.Team.insert(
        id=3, division=2, name="Atruc", shortcut="ATR",
        city="Plzeň", country="CZE"
    ).execute()
