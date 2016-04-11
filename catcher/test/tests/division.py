#!/usr/bin/python
# coding=utf-8

from testCase import TestCase
from falcon import HTTP_200, HTTP_201, HTTP_400
from catcher import models

class Divisions(TestCase):

    def testGet(self):
        divisions = len(models.Division.select())        
        response = self.request(
            method  = 'GET',
            path    = '/api/divisions',
            decode  = 'utf-8'
            )
        self.assertEqual(response['count'], divisions)
        self.assertEqual(self.srmock.status, HTTP_200)
        