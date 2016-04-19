#!/usr/bin/python
# coding=utf-8

from testCase import TestCase
from falcon import HTTP_200, HTTP_201, HTTP_400, HTTP_401
from catcher import models

class User(TestCase):

    def testPut1(self):
        '''edit email and password'''
        user = models.User.get(apiKey="#apiKey3")
        response = self.request(
            method  = 'PUT',
            path    = ('/api/user/%s' % user.id),
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "#apiKey3"
                },
            body    = {
                "email"   : "test2@test.cz",
                "oldPassword": "heslo1",
                "newPassword": "heslo2"
                }
            )

        self.assertEqual(response['id'], user.id)
        self.assertEqual(response['email'], "test2@test.cz")
        self.assertEqual(response['password'], "heslo2")
        self.assertEqual(self.srmock.status, HTTP_200)

    def testPut2(self):
        '''edit email and password'''
        user = models.User.get(apiKey="#apiKey3")
        response = self.request(
            method  = 'PUT',
            path    = ('/api/user/%s' % user.id),
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "#apiKey"
                },
            body    = {
                "email"   : "test2@test.cz",
                "newPassword": "heslo2"
                }
            )

        self.assertEqual(self.srmock.status, HTTP_400)

    def testPut3(self):
        '''edit email and password by invalid user'''
        user = models.User.get(apiKey="#apiKey")
        response = self.request(
            method  = 'PUT',
            path    = ('/api/user/%s' % (user.id + 1)),
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "#apiKey"
                },
            body    = {
                "email"   : "test2@test.cz",
                "newPassword": "heslo2"
                }
            )

        self.assertEqual(self.srmock.status, HTTP_401)


class Users(TestCase):

    def testPostOrganizer(self):
        '''create organizer'''
        # test new user (organizer)
        response = self.request(
            method  = 'POST',
            path    = '/api/users',
            headers = {"Content-Type": "application/json"},
            body    = {
                "email"   : "test2@test.cz",
                "password": "heslo1",
                "role"    : "organizer"
                }
            )
        self.assertEqual(self.srmock.status, HTTP_201)
        self.assertEqual(response['clubId'], None)
        self.assertEqual(response['email'], "test2@test.cz")
        self.assertEqual(response['role'], "organizer")

    def testPostClub(self):
        '''create club'''
        # test new user by admin
        response = self.request(
            method  = 'POST',
            path    = '/api/users',
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "#apiKey1"
                },
            body    = {
                "email"   : "test@test.cz",
                "password": "heslo1",
                "role"    : "club",
                "clubId"  : 1
                }
            )
        self.assertEqual(self.srmock.status, HTTP_201)
        self.assertEqual(response['clubId'], 1)
        self.assertEqual(response['email'], "test@test.cz")
        self.assertEqual(response['role'], "club")