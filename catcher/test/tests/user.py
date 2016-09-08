#!/usr/bin/python
# coding=utf-8

import falcon
import pytest

def test_user_get(client, models):
    user_id = models.User.insert(
        email='mickey@mouse.com',
        password="e8WFffXew",
        api_key="W1x8UmkV5RWCZOXuRmcqqnrt6qQNnjnr",
        role=1
    ).execute()
    resp = client.get('/api/user?id=%s' % user_id)
    assert resp.status == falcon.HTTP_OK
    assert resp.json['email'] == 'mickey@mouse.com'
    assert resp.json['password'] == None

def test_user_login(models, users):
    user = models.User.login("mickey@mouse.com", "e8WFffXew")
    assert user.email == "mickey@mouse.com"

def test_user_validate_email(models):
    models.User.validateEmail("test@seznam.cz")
    with pytest.raises(falcon.HTTPBadRequest):
        models.User.validateEmail("test@seznam")

def test_user_validate_password(models):
    models.User.validatePassword("123456")
    with pytest.raises(falcon.HTTPBadRequest):
        models.User.validatePassword("12345")


# import falcon.testing
# # from testCase import TestCase
# from falcon import HTTP_200, HTTP_201, HTTP_400, HTTP_401
# from catcher import models
# import logging


# print "database.name"

# class Sample(falcon.testing.TestCase):
#     def test1(self):
#         print "XXXXXXXXXXXXXX"
#         logging.debug("SSSSSSSSSS")
#         pass

# class User(TestCase):

#     def testPut1(self):
#         '''edit email and password'''
#         user = models.User.get(apiKey="#apiKey3")
#         response = self.request(
#             method  = 'PUT',
#             path    = ('/api/user/%s' % user.id),
#             headers = {
#                 "Content-Type" : "application/json",
#                 "Authorization": "#apiKey3"
#                 },
#             body    = {
#                 "email"   : "test33@test.cz",
#                 "oldPassword": "heslo3",
#                 "newPassword": "heslo33"
#                 }
#             )

#         self.assertEqual(response['id'], user.id)
#         self.assertEqual(response['email'], "test33@test.cz")
#         self.assertEqual(response['password'], "heslo33")
#         self.assertEqual(self.srmock.status, HTTP_200)

#     def testPut2(self):
#         '''edit email and password'''
#         user = models.User.get(apiKey="#apiKey3")
#         response = self.request(
#             method  = 'PUT',
#             path    = ('/api/user/%s' % user.id),
#             headers = {
#                 "Content-Type" : "application/json",
#                 "Authorization": "#apiKey3"
#                 },
#             body    = {
#                 "email"   : "test2@test.cz",
#                 "newPassword": "heslo2"
#                 }
#             )

#         self.assertEqual(self.srmock.status, HTTP_400)

#     def testPut3(self):
#         '''edit email and password by invalid user'''
#         user = models.User.get(apiKey="#apiKey1")
#         response = self.request(
#             method  = 'PUT',
#             path    = ('/api/user/%s' % (user.id + 1)),
#             headers = {
#                 "Content-Type" : "application/json",
#                 "Authorization": "#apiKey1"
#                 },
#             body    = {
#                 "email"   : "test2@test.cz",
#                 "newPassword": "heslo2"
#                 }
#             )

#         self.assertEqual(self.srmock.status, HTTP_401)


# class Users(TestCase):

#     def testPostOrganizer(self):
#         '''create organizer'''
#         # test new user (organizer)
#         response = self.request(
#             method  = 'POST',
#             path    = '/api/users',
#             headers = {"Content-Type": "application/json"},
#             body    = {
#                 "email"   : "test-organizer@test.cz",
#                 "password": "heslo1",
#                 "role"    : "organizer"
#                 }
#             )
#         self.assertEqual(self.srmock.status, HTTP_201)
#         self.assertEqual(response['clubId'], None)
#         self.assertEqual(response['email'], "test-organizer@test.cz")
#         self.assertEqual(response['role'], "organizer")

#     def testPostClub(self):
#         '''create club'''
#         # test new user by admin
#         response = self.request(
#             method  = 'POST',
#             path    = '/api/users',
#             headers = {
#                 "Content-Type" : "application/json",
#                 "Authorization": "#apiKey1"
#                 },
#             body    = {
#                 "email"   : "test@test.cz",
#                 "password": "heslo1",
#                 "role"    : "club",
#                 "clubId"  : 1
#                 }
#             )
#         self.assertEqual(self.srmock.status, HTTP_201)
#         self.assertEqual(response['clubId'], 1)
#         self.assertEqual(response['email'], "test@test.cz")
#         self.assertEqual(response['role'], "club")