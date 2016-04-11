#!/usr/bin/python
# coding=utf-8

# import ujson as json
import falcon.testing
from catcher import restapi
from catcher import resources as r
# from catcher import models as m
import logging
from test import Database
from playhouse.shortcuts import model_to_dict
import json


# TODO: in new Falcon version use TestCase instead TestBase
class TestCase(falcon.testing.TestBase):

    @staticmethod
    def modelToDict(model):
        return model_to_dict(model)

    @classmethod
    def setUpClass(cls):
        logging.debug("Called setUpClass")
        Database.fill()

    @classmethod
    def tearDownClass(cls):
        logging.debug("Called tearDownClass")
        Database.clean()

    def request(self, method, path, headers = None, body = None, decode = 'utf-8'):

        if isinstance(body, dict):
            body = json.dumps(body)
        
        response = self.simulate_request(
            method  = method,
            path    = path,
            headers = headers,
            body    = body,
            decode  = 'utf-8'
            )
        return json.loads(response) if response else None

    # it's called before each test
    def before(self):
        self.api = restapi.api