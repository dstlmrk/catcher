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
api.add_route('/club/{id}', r.Club(m.Club,['shortcut', 'city', 'country']))
api.add_route('/clubs', r.Clubs(m.Club))

api.add_route('/player/{id}', r.Player(m.Player,
    ['firstname', 'lastname', 'nickname', 'number', 'ranking']))
api.add_route('/players', r.Players(m.Player))

api.add_route('/division/{id}', r.Division(m.Division, ['division']))
api.add_route('/divisions', r.Divisions(m.Division))

api.add_route('/team/{id}', r.Team(m.Team, ['divisionId', 'degree']))
api.add_route('/teams', r.Teams(m.Team))

# TODO: dodelat
api.add_route('/tournament/{id}', r.Tournament(m.Tournament, []))
api.add_route('/tournaments', r.Tournaments(m.Tournament))
api.add_route('/createTournament', r.CreateTournament())

# errors
api.add_error_handler(Exception, errors.InternalServerError)
api.add_error_handler(TypeError, errors.BadRequest)
api.add_error_handler(KeyError, errors.BadRequest)
api.add_error_handler(ValueError, errors.BadRequest)
api.add_error_handler(m.MySQLModel.DoesNotExist, errors.NotFound)
api.add_error_handler(AttributeError, errors.BadRequest)