#!/usr/bin/python
# coding=utf-8

import falcon
import resources

from catcher import models
from catcher import errors
from catcher import middleware

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
api.add_route('/club/{id}', resources.Club(models.Club, ['shortcut', 'city', 'country']))
api.add_route('/clubs', resources.Clubs(models.Club))

api.add_route('/player/{id}', resources.Player(models.Player, ['firstname', 'lastname', 'nickname', 'number', 'ranking']))
api.add_route('/players', resources.Players(models.Player))

api.add_route('/division/{id}', resources.Division(models.Division, ['division']))
api.add_route('/divisions', resources.Divisions(models.Division))

api.add_route('/team/{id}', resources.Division(models.Team, ['divisionId', 'degree']))
api.add_route('/teams', resources.Divisions(models.Team))


api.add_error_handler(Exception, errors.InternalServerError)
api.add_error_handler(TypeError, errors.BadRequest)
api.add_error_handler(KeyError, errors.BadRequest)
api.add_error_handler(models.MySQLModel.DoesNotExist, errors.NotFound)
api.add_error_handler(AttributeError, errors.BadRequest)