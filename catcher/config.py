#!/usr/bin/python
# coding=utf-8

import configparser
import os
from catcher.logger import logger


class Config(configparser.ConfigParser):

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        app_abspath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../")
        logger.debug(app_abspath)
        self.read(app_abspath + '/conf/catcher.test.cfg')
        # it overwrites prior config file if exists
        self.read(app_abspath + '/conf/catcher.cfg')

config = Config()
