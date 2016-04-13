# #!/usr/bin/python
# # coding=utf-8

from catcher import logger
from catcher import models
from catcher import config
import os, sys
import logging
import unittest
from tests import *

class Database(object):

    # if you want change name of test database, you have to edit dataset file
    name   = config.testDb['name']
    host = config.testDb['host']
    wd   = os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def dump(db, host, user, passwd):
        dumpSuccess = True
        if 0 == os.system(
            "mysqldump --no-data --single-transaction"
            + " --host=\"%s\"" % host
            + " --user=\"%s\"" % user
            + " --password=\"%s\"" % passwd
            + " \"%s\"" % db
            + " > db.sql"):
            logging.debug("Dump is successfully created")
        else:
            sys.exit(logging.error("Dump is not created"))

    @classmethod
    def create(cls):
        init = ('''
        DROP SCHEMA IF EXISTS %s;\
        CREATE SCHEMA %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;\
        ''' % (cls.name, cls.name))

        if 0 != os.system("echo \"%s\" | mysql -h \"%s\"" % (init, cls.host)):
            sys.exit(logging.error("Test database is not created (init script)"))
        if 0 != os.system("mysql -h \"%s\" -D \"%s\" < \"%s/db.sql\"" % (cls.host, cls.name, cls.wd)):
            sys.exit(logging.error("Test database is not created (dump file)"))
        logging.debug("Test database is successfully created")

    @classmethod
    def fill(cls):
        if 0 != os.system("mysql -h \"%s\" -D \"%s\" < \"%s/dataset.sql\"" % (cls.host, cls.name, cls.wd)):
            sys.exit(logging.error("Dataset is not imported"))
        logging.debug("Dataset is imported")

    @classmethod
    def removeTemporaryFiles(cls):
        if 0 != os.system("rm \"%s/db.sql\"" % (cls.wd)):
            sys.exit(logging.error("Dump file is deleted"))
        logging.debug("Dump file is deleted")

    @classmethod
    def delete(cls):
        models.db.execute_sql("DROP DATABASE IF EXISTS `%s`" % cls.name)
        qr = models.db.execute_sql("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA " +
            "WHERE SCHEMA_NAME = '%s'" % cls.name)
        if len(qr.fetchall()) == 0:
            logging.debug("Test database is deleted")
        else:
            logging.error("Test database is not deleted")

    @staticmethod
    def clean():
        models.db.execute_sql("SET foreign_key_checks = 0")
        qr = models.db.execute_sql("SHOW TABLES")
        for table in qr.fetchall():
            name = table[0]
            models.db.execute_sql("DELETE FROM `" + name + "`")
        models.db.execute_sql("SET foreign_key_checks = 1")
        logging.debug("Tables are cleaned")

class Result(object):

    @staticmethod
    def success(str):
        return '\033[92m\033[1m' + "OK: " + str + '\033[0m'

    @staticmethod
    def fail(str):
        return '\033[91m\033[1m' + "FAIL: " + str + '\033[0m'

    @staticmethod
    def lineWrap(str):
        line = '='*80
        return line + '\n' + str + '\n' + line

    @staticmethod
    def pprint(res):
        rp          = Result
        errors      = res.result.errors
        failures    = res.result.failures
        tests       = res.result.testsRun
        errMethods  = ""
        failMethods = ""

        for e in errors:
            errMethods = errMethods + "   - " + str(e[0]) + '\n'

        for f in failures:
            failMethods = failMethods + "   - " + str(f[0]) + '\n'

        info = " %d errors\n%s %d failures\n%s %d tests" \
            % (len(errors), errMethods, len(failures), failMethods, tests)

        if res.result.wasSuccessful():
            print rp.lineWrap(rp.success(
                "All tests were successfully completed:\n" + info
                ))
        else:
            sys.exit(rp.lineWrap(rp.fail(
                "All tests weren't successfully completed:\n" + info
                )))

if __name__ == '__main__':
    # dump database in ./db.sql file
    Database.dump(
        config.db['name'],
        config.db['host'],
        config.db['user'],
        config.db['passwd']
        )
    # create test database
    Database.create()
    # run tests
    result = unittest.main(exit=False)
    # clean working directory from tmp files
    Database.removeTemporaryFiles()
    # Database.delete()
    # print results
    Result.pprint(result)
