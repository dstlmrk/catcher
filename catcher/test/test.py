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
        email='mickey@mouse.com',
        password="e8WFffXew",
        role="organizer"
    )
    models.User.create(
        email='adam@mouse.com',
        password="T3Cfp9HYt",
        role="organizer"
    )
