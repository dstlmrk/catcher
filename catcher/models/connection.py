#!/usr/bin/python
# coding=utf-8

import inspect
from peewee import MySQLDatabase
from catcher import config
import logging


def connect_database():
    test = False
    # check, if this import is not called by test files
    curframe = inspect.currentframe()
    for x in inspect.getouterframes(curframe):
        if "test.py" in x[1]:
            test = True
    if not test:
        db = MySQLDatabase(
            config.db['name'],
            user=config.db['user'],
            passwd=config.db['passwd'],
            host=config.db['host']
            )
        logging.debug("Connected Catcher database")
    else:
        db = MySQLDatabase(
            config.testDb['name'],
            user=config.testDb['user'],
            passwd=config.testDb['passwd'],
            host=config.testDb['host']
            )
        logging.debug("Connected test database %s" % config.testDb['name'])
    return db
