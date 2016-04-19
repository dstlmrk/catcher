#!/usr/bin/python
# coding=utf-8

from testCase import TestCase
from falcon import HTTP_200, HTTP_201, HTTP_400
from catcher import models

class User(TestCase):

    def before(self):
        models.User(
            email    = "email-organizer@test.cz",
            password = "heslo1",
            apiKey   = "#apiKey111",
            role     = "organizer"
            ).save()

    def testPost(self):
        '''login'''
        print "VOLAM..."
        response = self.request(
            method  = 'POST',
            path    = '/api/login',
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "#apiKey111"
            },
            body    = {
                "email"   : "email-organizer@test.cz",
                "password": "heslo1"
                }
            )
        print response
        self.assertEqual(self.srmock.status, HTTP_200)
        self.assertEqual(response['email'], "email-organizer@test.cz")
        self.assertEqual(response['apiKey'], "#apiKey111")
        self.assertEqual(response['password'], "heslo1")
        self.assertEqual(response['role'], "organizer")
        self.assertEqual(response['clubId'], None)
