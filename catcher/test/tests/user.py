#!/usr/bin/python
# coding=utf-8

from testCase import TestCase
from falcon import HTTP_200, HTTP_201, HTTP_400
from catcher import models

class User(TestCase):
    pass
    # def testPut(self):
        # ''''''
        # self.assertEqual(response, expectedResponse)
        # self.assertEqual(self.srmock.status, HTTP_201)


class Users(TestCase):

    def before(self):
        models.Role(role="organizer").save()
        models.Role(role="admin").save()
        models.Role(role="club").save()
        models.User(
            email    = "admin@admin.cz",
            password = "hesloAdmin",
            apiKey   = "#apiKey",
            role     = "admin"
            ).save()

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
        # test new user (organizer)
        response = self.request(
            method  = 'POST',
            path    = '/api/users',
            headers = {"Content-Type": "application/json", "Authorization": "#apiKey"},
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


# TODO: napsat classu Login, kde overim prihlaseni a funkcnost apiKey