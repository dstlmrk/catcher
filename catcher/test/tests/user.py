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
    assert resp.json['api_key'] == None


def test_user_put_passwd_change(client, models):
    user_id = models.User.insert(
        email='mickey@mouse.com',
        password="e8WFffXew",
        api_key="W1x8UmkV5RWCZOXuRmcqqnrt6qQNnjnr",
        role=1
    ).execute()
    resp = client.put(
        '/api/user?id=%s' % user_id,
        {'old_password': "e8WFffXew", 'new_password': "3kQp54FrT"},
        headers={
            "Content-Type": "application/json",
            "Authorization": "W1x8UmkV5RWCZOXuRmcqqnrt6qQNnjnr"
        }
    )
    assert resp.status == falcon.HTTP_OK
    assert resp.json['email'] == 'mickey@mouse.com'
    assert resp.json['password'] == None
    user = models.User.login("mickey@mouse.com", "3kQp54FrT")
    assert user.email == "mickey@mouse.com"


def test_user_put_email_change(client, models):
    user_id = models.User.insert(
        email='mickey@mouse.com',
        password="e8WFffXew",
        api_key="W1x8UmkV5RWCZOXuRmcqqnrt6qQNnjnr",
        role=1
    ).execute()
    resp = client.put(
        '/api/user?id=%s' % user_id, {'email': "lisa@mouse.com"},
        headers={
            "Content-Type": "application/json",
            "Authorization": "W1x8UmkV5RWCZOXuRmcqqnrt6qQNnjnr"
        }
    )
    assert resp.status == falcon.HTTP_OK
    assert resp.json['email'] == 'lisa@mouse.com'
    assert resp.json['password'] == None
    user = models.User.login("lisa@mouse.com", "e8WFffXew")
    assert user.email == "lisa@mouse.com"


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


def test_users_get(client, models):
    models.User.insert(
        email='user1@test.cz',
        password="e8WFffXew",
        api_key="#apiKey1",
        role=1
    ).execute()
    models.User.insert(
        email='user2@test.cz',
        password="3kQp54FrT",
        api_key="#apiKey2",
        role=1
    ).execute()
    models.User.insert(
        email='user3@test.cz',
        password="215p54315",
        api_key="#apiKey3",
        role=1
    ).execute()
    models.User.insert(
        email='user4@test.cz',
        password="fkpRt4FrT",
        api_key="#apiKey4",
        role=1
    ).execute()
    resp = client.get('/api/users')

    assert resp.status == falcon.HTTP_OK
    assert len(resp.json['users']) == 4
    assert resp.json['users'][3]['email'] == "user4@test.cz"
    assert resp.json['users'][0]['password'] == None


def test_users_post(client, models):
    '''Registration test'''
    resp = client.post(
        '/api/users',
        {
            'email': "mickey@mouse.com",
            'password': "e8WFffXew",
            'role': "organizer"
        },
        headers={
            "Content-Type": "application/json"
        }
    )
    assert resp.status == falcon.HTTP_201
    user = models.User.get(email="mickey@mouse.com")
    assert user.email == "mickey@mouse.com"
    assert user.role.role == "organizer"
