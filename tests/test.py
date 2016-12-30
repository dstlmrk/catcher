# #!/usr/bin/python
# # coding=utf-8

from tests.models import *

from catcher.config import config
# from database import Database
from tests.database import Database
import pytest

print("test.py")

import logging
# TODO: udelat logging nejaky barevnejsi

# TODO: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# TODO: pokracovat logovanim, abych videl, co se v testech kdyztak deje

logging.basicConfig(level=logging.DEBUG)

logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything


# print(user.a)
# # from catcher import logger
# from catcher import models as catcher_models
# from catcher import config
# from catcher import restapi
# from catcher.test.database import Database
# import pytest
#
# from catcher.
#
#
# # from tests import *
#
#


# import PyMySQL
#
# # Open database connection
# db = pymysql.connect(
#     config['db']['host'],
#     config['db']['user'],
#     config['db']['password'],
#     config['db']['name']
# )
#
# cursor = db.cursor()
#
# cursor.execute("SELECT * FROM catcher.user")
#
# data = cursor.fetchall()
#
# for d in data:
#     print(d)
#
# db.close()



@pytest.yield_fixture(scope='session')
def database():
    database = Database(
        config['db']['name'],
        config['db']['host'],
        config['db']['user'],
        config['db']['password'],
    )
    database.dump()
    database.create()
    yield database
    # database.remove_temp_files()
    # database.delete()


@pytest.yield_fixture(scope='function')
def db(database):
    # database.fill()
    yield True
    # database.clean()


# @pytest.fixture
# def app(db):
#     '''It uses for falcon testing'''
#     restapi.api.req_options.auto_parse_form_urlencoded = True
#     return restapi.api


@pytest.fixture
def models(db):
    return True
    return catcher_models
#
#
# @pytest.fixture(scope='function')
# def users(models):
#     models.User.insert(
#         id=1,
#         email='mickey@mouse.com',
#         password="e8WFffXew",
#         role=1, # organizer
#         api_key="#apiKeyOrganizer1"
#     ).execute()
#     models.User.insert(
#         id=2,
#         email='adam@mouse.com',
#         password="T3Cfp9HYt",
#         role=1, # organizer
#         api_key="#apiKeyOrganizer2"
#     ).execute()
#     models.User.insert(
#         id=3,
#         email='admin@catcher.cz',
#         password="Rf3;c9HYt",
#         role=2, # admin
#         api_key="#apiKeyAdmin"
#     ).execute()
#
#
# @pytest.fixture(scope='function')
# def teams(models, users):
#     models.Team.insert(
#         id=1, division=1, name="Frozen Angels", shortcut="FAL",
#         city="Liberec", country="CZE", user_id=1,
#     ).execute()
#     models.Team.insert(
#         id=2, division=2, name="KeFEAR", shortcut="KEF",
#         city="Košice", country="SVK", user_id=2,
#     ).execute()
#     models.Team.insert(
#         id=3, division=2, name="Atruc", shortcut="ATR",
#         city="Plzeň", country="CZE"
#     ).execute()
