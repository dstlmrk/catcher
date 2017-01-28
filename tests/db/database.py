#!/usr/bin/python
# coding=utf-8

from catcher.logger import logger
import os
import sys
import pymysql


class Database(object):
    """Represents test database"""

    def __init__(self, name, host, user, passwd):
        self.original_name = name
        self.name = "test_" + name
        self.host = "127.0.0.1"
        self.user = user
        self.passwd = passwd
        self.wd = os.path.dirname(os.path.realpath(__file__))

    def dump(self):
        if 0 == os.system((
            "mysqldump --no-data --single-transaction"
            " --host=\"{}\" --user=\"{}\" --password=\"{}\" \"{}\" > \"{}/dump.sql\""
            ).format(
                self.host, self.user, self.passwd, self.original_name, self.wd
            )
        ):
            logger.debug("Dump is successfully created")
        else:
            logger.warn("Dump is not created so the old is used")
            # sys.exit(logger.error("Dump is not created"))

    def create(self):

        logger.warn(os.system("printenv"))
        logger.debug(self.host + " " + self.user + " " + self.passwd + " " + self.name)
        os.system("mysql -e 'CREATE DATABASE test_catcher;'")
        self.conn = pymysql.connect(self.host, self.user, self.passwd, self.name)
        c = self.conn.cursor()
        logger.debug("======================")
        # c.commit()
        c.execute("SHOW SCHEMAS")
        logger.debug(c.fetchall())
        c.execute("USE test_catcher")
        c.execute("SHOW TABLES")
        logger.debug(c.fetchall())

        # init = (
        #     # 'DROP SCHEMA IF EXISTS %s;'
        #     'CREATE SCHEMA %s DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;'
        #     % (self.name, self.name)
        # )
        # cmd = ("echo \"%s\" | mysql -h \"%s\"" % (init, self.host))
        # if 0 != os.system(cmd):
        #     sys.exit(
        #         logger.error("Test database is not created (init script)")
        #     )
        # logger.debug(cmd)
        cmd = ("mysql -h \"%s\" -D \"%s\" < \"%s/dump.sql\"" % (self.host, self.name, self.wd))
        if 0 != os.system(cmd):
            sys.exit(
                logger.error("Test database is not created (dump file)")
            )

        # logger.debug(cmd)

        # self.conn = pymysql.connect(self.host, self.user, self.passwd, self.name)
        # c = self.conn.cursor()
        c.execute("SHOW SCHEMAS")
        logger.debug(c.fetchall())
        c.execute("USE test_catcher")
        c.execute("SHOW TABLES")
        logger.debug(c.fetchall())
        c.close()

        logger.debug("Test database is successfully created")

    def fill(self):
        cmd = ("mysql -h \"%s\" -D \"%s\" < \"%s/dataset.sql\"" % (self.host, self.name, self.wd))
        if 0 != os.system(cmd):
            logger.debug(cmd)
            sys.exit(logger.error("Dataset is not imported"))
        logger.debug("Dataset is imported")

    def remove_temp_files(self):
        if 0 != os.system("rm \"%s/dump.sql\"" % (self.wd)):
            sys.exit(logger.error("Dump file is deleted"))
        logger.debug("Dump file is deleted")

    def delete(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP DATABASE IF EXISTS `%s`" % self.name)
        cursor.execute(
            "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA " +
            "WHERE SCHEMA_NAME = \"%s\"" % self.name
        )
        if len(cursor.fetchall()) == 0:
            logger.debug("Test database is deleted")
        else:
            logger.error("Test database is not deleted")
        cursor.close()

    def clean(self):
        cursor = self.conn.cursor()
        cursor.execute("SET foreign_key_checks = 0")
        cursor.execute("SHOW TABLES")
        for table in cursor.fetchall():
            name = table[0]
            cursor.execute("DELETE FROM `" + name + "`")
        cursor.execute("SET foreign_key_checks = 1")
        logger.debug("Tables are cleaned")
        cursor.close()
