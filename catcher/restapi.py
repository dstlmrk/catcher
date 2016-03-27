#!/usr/bin/python
# coding=utf-8

import falcon
import resources as r

from catcher import models as m
from catcher import errors
from catcher import middleware

# print all queries to stderr
import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

'''
falcon.API instances are callable WSGI apps

Each component’s process_request, process_resource, and process_response
methods are executed hierarchically, as a stack, following the ordering of the list
passed via the middleware kwarg of falcon.API.
'''
api = falcon.API(middleware=[
    middleware.PeeweeConnection(),
    # middleware.Authorization(),
    middleware.RequireJSON(),
    middleware.JSONTranslator(),
])

# resources are represented by long-lived class instances
# TODO: editable cols presunout nekam, kde je muzu upravovat zaroven i pro testy
api.add_route('/api/club/{id}', r.Club(m.Club,['shortcut', 'city', 'country']))

api.add_route('/api/clubs', r.Clubs(m.Club))

api.add_route('/api/player/{id}', r.Player(m.Player,
    ['firstname', 'lastname', 'nickname', 'number', 'ranking']))
api.add_route('/api/players', r.Players(m.Player))

api.add_route('/api/division/{id}', r.Division(m.Division, ['division']))
api.add_route('/api/divisions', r.Divisions(m.Division))

api.add_route('/api/team/{id}', r.Team(m.Team, ['divisionId', 'degree']))
api.add_route('/api/teams', r.Teams(m.Team))

# TODO: pomalu bych mel nekam psat, co ktera metoda udela.. dokumentace!
api.add_route('/api/tournament/{id}', r.Tournament(m.Tournament, []))
api.add_route('/api/tournaments', r.Tournaments(m.Tournament))
api.add_route('/api/tournaments/create', r.CreateTournament())
api.add_route('/api/tournament/{id}/active', r.ActiveTournament())

api.add_route('/api/tournament/{id}/standings', r.Standings())

api.add_route('/api/match/{id}', r.Match(m.Match,[]))
api.add_route('/api/matches', r.Matches(m.Match))

# errors
api.add_error_handler(Exception, errors.InternalServerError)
api.add_error_handler(TypeError, errors.BadRequest)
api.add_error_handler(KeyError, errors.BadRequest)
api.add_error_handler(ValueError, errors.BadRequest)
api.add_error_handler(m.MySQLModel.DoesNotExist, errors.NotFound)
api.add_error_handler(AttributeError, errors.BadRequest)