#!/usr/bin/python
# coding=utf-8

import logging
import colorlog

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(purple)s%(asctime)s %(cyan)s%(name)s%(white)s [%(levelname)s] %(log_color)s%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
)

# sqlalchemy logging
sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
sqlalchemy_logger.setLevel('INFO')
sqlalchemy_logger.addHandler(handler)

# catcher logging
logger = colorlog.getLogger('catcher')
logger.addHandler(handler)
