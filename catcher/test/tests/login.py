#!/usr/bin/python
# coding=utf-8

from testCase import TestCase
from falcon import HTTP_200, HTTP_201, HTTP_400
from catcher import models

class User(TestCase):

    def before(self):
        models.Role(role="organizer").save()
        models.Role(role="admin").save()
        models.Role(role="club").save()
        models.User(
            email    = "test@test.cz",
            password = "heslo1",
            apiKey   = "#apiKey",
            role     = "organizer"
            ).save()

    def testPost(self):
        '''login'''
        response = self.request(
            method  = 'POST',
            path    = '/api/login',
            headers = {"Content-Type" : "application/json"},
            body    = {
                "email"   : "test@test.cz",
                "password": "heslo1"
                }
            )
        print response
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['email'], "test@test.cz")
        self.assertEqual(response['apiKey'], "#apiKey")
        self.assertEqual(response['password'], "heslo1")
        self.assertEqual(response['role'], "organizer")
        self.assertEqual(response['clubId'], None)
