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
    middleware.Authorization(),
    middleware.RequireJSON(),
    middleware.JSONTranslator(),
])

# resources are represented by long-lived class instances
api.add_route('/club/{id}', resources.Club(models.Club, ['shortcut', 'city', 'country']))
api.add_route('/clubs', resources.Clubs())

api.add_error_handler(Exception, errors.InternalServerError)
api.add_error_handler(TypeError, errors.BadRequest)
api.add_error_handler(KeyError, errors.BadRequest)
api.add_error_handler(models.MySQLModel.DoesNotExist, errors.NotFound)