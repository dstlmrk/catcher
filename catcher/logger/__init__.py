#!/usr/bin/python
# coding=utf-8

import logging
from loggingStreamHandler import ColorizingStreamHandler
from catcher import config

root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(ColorizingStreamHandler())

# logging.debug('DEBUG')
# logging.info('INFO')
# logging.warning('WARNING')
# logging.error('ERROR')
# logging.critical('CRITICAL')