# #!/usr/bin/python
# # coding=utf-8

from catcher import logger
from catcher import models as catcher_models
from catcher import config
from catcher import restapi
import os
import sys
import logging
import pytest

# import unittest
from tests import *


class Database(object):

    def __init__(self, name, host, user, passwd, connection):
        self.original_name = name
        self.name = "test_" + name
        self.host = host
        self.user = user
        self.passwd = passwd
        self.wd = os.path.dirname(os.path.realpath(__file__))
        self.connection = connection

    def dump(self):
        if 0 == os.system(
            "mysqldump --no-data --single-transaction"
            + " --host=\"%s\"" % self.host
            + " --user=\"%s\"" % self.user
            + " --password=\"%s\"" % self.passwd
            + " \"%s\"" % self.original_name
            + " > db.sql"):
            logging.debug("Dump is successfully created")
        else:
            sys.exit(logging.error("Dump is not created"))

    def create(self):
        init = (
            '''DROP SCHEMA IF EXISTS %s;\
            CREATE SCHEMA %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;\
            ''' % (self.name, self.name)
        )

        if 0 != os.system(
            "echo \"%s\" | mysql -h \"%s\"" % (init, self.host)
        ):
            sys.exit(
                logging.error("Test database is not created (init script)")
            )
        if 0 != os.system(
            "mysql -h \"%s\" -D \"%s\" < \"%s/db.sql\"" % (
                self.host, self.name, self.wd)
        ):
            sys.exit(
                logging.error("Test database is not created (dump file)")
            )
        logging.debug("Test database is successfully created")

    def fill(self):
        if 0 != os.system("mysql -h \"%s\" -D \"%s\" < \"%s/dataset.sql\"" % (self.host, self.name, self.wd)):
            sys.exit(logging.error("Dataset is not imported"))
        logging.debug("Dataset is imported")

    def remove_temp_files(self):
        if 0 != os.system("rm \"%s/db.sql\"" % (self.wd)):
            sys.exit(logging.error("Dump file is deleted"))
        logging.debug("Dump file is deleted")

    def delete(self):
        self.connection.execute_sql("DROP DATABASE IF EXISTS `%s`" % self.name)
        qr = self.connection.execute_sql(
            "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA " +
            "WHERE SCHEMA_NAME = '%s'" % self.name
        )
        if len(qr.fetchall()) == 0:
            logging.debug("Test database is deleted")
        else:
            logging.error("Test database is not deleted")

    def clean(self):
        self.connection.execute_sql("SET foreign_key_checks = 0")
        qr = self.connection.execute_sql("SHOW TABLES")
        for table in qr.fetchall():
            name = table[0]
            self.connection.execute_sql("DELETE FROM `" + name + "`")
        self.connection.execute_sql("SET foreign_key_checks = 1")
        logging.debug("Tables are cleaned")

# class TestCase(falcon.testing.TestCase):

#     def request(self, method, path, headers = None, body = None, decode = 'utf-8', queryString = None):

#         if isinstance(body, dict):
#             body = json.dumps(body)
        
#         response = self.simulate_request(
#             method       = method,
#             path         = path,
#             headers      = headers,
#             body         = body,
#             decode       = decode,
#             query_string = queryString 
#             )
#         return json.loads(response) if response else None

#     def setUp(self):
#         Database.fill()

#         models.Role(role="organizer").save()
#         models.Role(role="admin").save()
#         models.Role(role="club").save()
#         models.User(
#             email    = "test1@test.cz",
#             password = "heslo1",
#             apiKey   = "#apiKey1",
#             role     = "admin"
#             ).save()
#         models.User(
#             email    = "test2@test.cz",
#             password = "heslo2",
#             apiKey   = "#apiKey2",
#             role     = "club",
#             clubId   = 1
#             ).save()
#         models.User(
#             email    = "test3@test.cz",
#             password = "heslo3",
#             apiKey   = "#apiKey3",
#             role     = "organizer"
#             ).save()
#         # database has to be filled before call before()
#         super(TestCase, self).setUp()
#         # api has to be after super
#         self.api = restapi.api

#     def tearDown(self):
#         super(TestCase, self).tearDown()
#         database.clean()

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
    """
    Slouzi pro testovani falconu
    """
    restapi.api.req_options.auto_parse_form_urlencoded = True
    return restapi.api

@pytest.fixture
def models(db):
    return catcher_models

@pytest.fixture(scope='function')
def users(models):
    # models.Role.create(id=1, role="admin")
    models.User.create(email='mickey@mouse.com', password="e8WFffXew")
    models.User.create(email='adam@mouse.com', password="T3Cfp9HYt")
    # return catcher_models
