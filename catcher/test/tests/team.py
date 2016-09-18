#!/usr/bin/python
# coding=utf-8

import falcon
import pytest


def test_team_get(client, models, users):
    team_id = models.Team.insert(
        division=1, name="Frozen Angels", shortcut="FAL",
        city="Liberec", country="CZE", user_id=1,
    ).execute()
    resp = client.get('/api/team/%s' % team_id)
    expected_resp = {
        'id': team_id,
        'name': 'Frozen Angels',
        'cald_id': None,
        'country': 'CZE',
        'shortcut': 'FAL',
        'city': 'Liberec',
        'user_id': 1,
        'division': {
            'division': 'open',
            'id': 1
        }
    }
    print resp.json
    assert resp.status == falcon.HTTP_OK
    assert resp.json == expected_resp


def test_team_put(client, teams):
    resp = client.put(
        '/api/team/%s' % 1,
        {'name': "FC Liberec", 'city': None},
        # TODO: mel by upravovat admin nebo majitel tymu
        # "Authorization": "W1x8UmkV5RWCZOXuRmcqqnrt6qQNnjnr"
        headers={
            "Content-Type": "application/json"
        }
    )
    assert resp.status == falcon.HTTP_OK
    assert resp.json['name'] == "FC Liberec"
    assert resp.json['shortcut'] == "FAL"
    assert resp.json['city'] == None


def test_team_delete(client, teams):
    teams_count = len(client.get('/api/teams').json['teams'])
    resp = client.delete(
        '/api/team/%s' % 1,
        headers={
            "Authorization": "#apiKeyAdmin"
        }
    )
    assert resp.status == falcon.HTTP_OK
    resp = client.get('/api/teams')
    assert len(resp.json['teams']) == teams_count - 1


def test_teams_get(client, teams):
    resp = client.get('/api/teams')
    assert resp.status == falcon.HTTP_OK
    assert len(resp.json['teams']) == 3
    assert resp.json['teams'][0]['name'] == "Frozen Angels"
    assert resp.json['teams'][1]['country'] == "SVK"
    assert resp.json['teams'][1]['cald_id'] == None
    assert resp.json['teams'][2]['division']['division'] == "women"
    assert resp.json['teams'][2]['city'] == u"Plzeň"


def test_specific_teams_get(client, teams):
    resp = client.get('/api/teams?city=Liberec&country=CZE')
    print resp.json
    assert resp.status == falcon.HTTP_OK
    assert len(resp.json['teams']) == 1
    assert resp.json['teams'][0]['name'] == "Frozen Angels"
    assert resp.json['teams'][1]['country'] == "CZE"


def test_specific_teams_get(client, teams):
    resp = client.get('/api/teams?division_id=2')
    print resp.json
    assert resp.status == falcon.HTTP_OK
    assert len(resp.json['teams']) == 2
    assert resp.json['teams'][0]['division']['id'] == 2


def test_teams_post(client, models):
    resp = client.post(
        '/api/teams',
        {
            'name': "FC Ostrava",
            'shortcut': "XXXX",
            'division': "open",
            'id': 999
        },
        headers={
            "Content-Type": "application/json"
        }
    )
    print resp.json
    assert resp.status == falcon.HTTP_201
    assert resp.json['id'] != 999
    assert resp.json['name'] == "FC Ostrava"
    assert resp.json['shortcut'] == "XXX"
    assert resp.json['division']['division'] == "open"
    assert resp.json['city'] == None
