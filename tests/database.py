#!/usr/bin/python
# coding=utf-8

# from catcher import logger
import logging
import os
import sys
import pymysql


class Database(object):

    def __init__(self, name, host, user, passwd):
        self.original_name = name
        self.name = "test_" + name
        self.host = host
        self.user = user
        self.passwd = passwd
        self.wd = os.path.dirname(os.path.realpath(__file__))
        self.connection = pymysql.connect(
            host, user, passwd, name
        )

        print("-----------")

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
