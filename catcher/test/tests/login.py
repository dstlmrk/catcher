#!/usr/bin/python
# coding=utf-8

import falcon
import pytest


def test_login_post(client, models):
    user_id = models.User.insert(
        email='mickey@mouse.com',
        password="e8WFffXew",
        api_key="W1x8UmkV5RWCZOXuRmcqqnrt6qQNnjnr",
        role=1
    ).execute()
    resp = client.post(
        '/api/login',
        {
            'email': "mickey@mouse.com",
            'password': "e8WFffXew"
        },
        headers={
            "Content-Type": "application/json"
        }
    )
    assert resp.status == falcon.HTTP_OK
    assert resp.json['email'] == "mickey@mouse.com"
    assert resp.json['password'] == None
    assert isinstance(resp.json['role'], dict)
    assert resp.json['api_key'] == "W1x8UmkV5RWCZOXuRmcqqnrt6qQNnjnr"


def test_forgotten_password_post():
    '''TODO: potreba mockovat odesilani emailu'''
    pass
