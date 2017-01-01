#!/usr/bin/python
# coding=utf-8

# TODO: vytvorit singleton na prijem configu

import sqlalchemy
import falcon
# import logger

# import logging
# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
# logging.debug('This message should appear on the console')
# logging.info('So should this')
# logging.warning('And this, too')

from catcher.api import middleware
from catcher import resources

# from resources.team import Team

# import .resources
# from .resources import team
# import catcher.resources
# from resources import Team

# from resources import Team
# import catcher.resources
# # from catcher.api import errors
# # from catcher.api import middleware
# # from catcher import resources
# # from catcher import models as m
# # import peewee as pw
#

# print("Hello")

'''
falcon.API instances are callable WSGI apps

Each component’s process_request, process_resource, and process_response
methods are executed hierarchically, as a stack, following the ordering of the list
passed via the middleware kwarg of falcon.API.
'''
api = falcon.API(
    middleware=[
        middleware.Crossdomain(),
        middleware.Authorization(),
        middleware.RequireJSON(),
        middleware.JSONTranslator(),
        ]
    )

# TODO: stahnut uwsgi a tady pak pokracovat
api.add_route('/api/team/{id}', resources.Team())

api.add_route('/api/user/{id}', resources.User())
api.add_route('/api/users', resources.Users())

# # resources are represented by long-lived class instances
# api.add_route('/api/club/{id}',  resources.Club(m.Club))
# # api.add_route('/api/club/{id}/players',  resources.ClubPlayers())
# # api.add_route('/api/club/{id}/teams',  resources.ClubTeams())
# # api.add_route('/api/clubs',  resources.Clubs(m.Club))
#
# # api.add_route('/api/player/{id}',  resources.Player(m.Player))
# # api.add_route('/api/players',  resources.Players(m.Player))
#
# # api.add_route('/api/divisions',  resources.Divisions(m.Division))
#
# api.add_route('/api/team/{id}', resources.Team())
# api.add_route('/api/teams', resources.Teams())
#
# # api.add_route('/api/tournaments',  resources.Tournaments(m.Tournament))
# # api.add_route('/api/tournament/{id}',  resources.Tournament(m.Tournament))
# # api.add_route('/api/tournament/{id}/standings',  resources.Standings())
# # api.add_route('/api/tournament/{id}/players',  resources.TournamentPlayers())
# # api.add_route('/api/tournament/{id}/teams',  resources.TournamentTeams())
# # api.add_route('/api/tournament/{id}/matches',  resources.TournamentMatches())
# # api.add_route('/api/tournament/{id}/spirits',  resources.Spirits())
# # api.add_route('/api/tournament/{id}/missing-spirits',  resources.MissingSpirits())
#
# # api.add_route('/api/match/{id}',  resources.Match(m.Match))
# # api.add_route('/api/match/{id}/points',  resources.MatchPoints())
# # api.add_route('/api/match/{id}/point/{order}',  resources.MatchPoint())
# # api.add_route('/api/match/{id}/spirits',  resources.Spirit())
#
# # api.add_route("/api/users", resources.Users())
# # api.add_route("/api/user/{id}", resources.User())
#
# api.add_route("/api/login", resources.Login())
# api.add_route("/api/forgotten-password", resources.ForgottenPassword())
#
# # api.add_route('/api/tournament/{id}/groups', resources.TournamentGroups())
# # api.add_route('/api/tournament/{id}/group/{ide}', resources.TournamentGroup())
#
# api.add_route("/api/users", resources.Users())
# api.add_route("/api/user", resources.User())
#

# def BadRequest(ex, req, resp, params):
# 	traceback.print_exc()
# 	raise falcon.HTTPBadRequest(
# 		ex.__class__.__name__,)
# 		)

# # errors
# # TODO: doplnit, podivat se do dokumentace na vyhazovani vyjimek
# api.add_error_handler(Exception, falcon.HTTPInternalServerError('1','2'))
# api.add_error_handler(sqlalchemy.exc.IntegrityError, falcon.HTTPInternalServerError(None, None))

# api.add_error_handler(RuntimeError, errors.InternalServerError)
# api.add_error_handler(TypeError, errors.BadRequest)
# api.add_error_handler(KeyError, errors.BadRequest)
# api.add_error_handler(ValueError, errors.BadRequest)
# api.add_error_handler(AttributeError, errors.BadRequest)