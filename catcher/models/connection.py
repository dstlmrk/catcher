#!/usr/bin/python
# coding=utf-8

import inspect
import peewee
from catcher import config
import logging

def connectDatabase():
    test = False
    # check, if this import is not called by test files
    curframe = inspect.currentframe()
    for x in inspect.getouterframes(curframe):
        if "test.py" in x[1]:
            test = True

    if not test:
        db = peewee.MySQLDatabase(
                     config.db['name'],
            user   = config.db['user'],
            passwd = config.db['passwd'],
            host   = config.db['host']
            )
        logging.debug("Connected Catcher database")
    else:
        db = peewee.MySQLDatabase(
                     config.testDb['name'],
            user   = config.testDb['user'],
            passwd = config.testDb['passwd'],
            host   = config.testDb['host']
            )

        logging.debug("Connected test database %s" % config.testDb['name'])

    return db
