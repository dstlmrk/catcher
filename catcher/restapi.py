#!/usr/bin/python
# coding=utf-8

import logger
import falcon
from catcher.api import errors
from catcher.api import middleware
from catcher import resources
from catcher import models as m
import peewee as pw

'''
falcon.API instances are callable WSGI apps

Each component’s process_request, process_resource, and process_response
methods are executed hierarchically, as a stack, following the ordering of the list
passed via the middleware kwarg of falcon.API.
'''
api = falcon.API(
    middleware = [
        middleware.Crossdomain(),
        middleware.PeeweeConnection(),
        middleware.Authorization(),
        middleware.RequireJSON(),
        middleware.JSONTranslator(),
        ]
    )

# resources are represented by long-lived class instances
api.add_route('/api/club/{id}',  resources.Club(m.Club))
api.add_route('/api/club/{id}/players',  resources.ClubPlayers())
api.add_route('/api/club/{id}/teams',  resources.ClubTeams())
api.add_route('/api/clubs',  resources.Clubs(m.Club))

api.add_route('/api/player/{id}',  resources.Player(m.Player))
api.add_route('/api/players',  resources.Players(m.Player))

api.add_route('/api/divisions',  resources.Divisions(m.Division))

api.add_route('/api/team/{id}',  resources.Team(m.Team))
api.add_route('/api/teams',  resources.Teams(m.Team))

api.add_route('/api/tournaments',  resources.Tournaments(m.Tournament))
api.add_route('/api/tournament/{id}',  resources.Tournament(m.Tournament))
api.add_route('/api/tournament/{id}/standings',  resources.Standings())
api.add_route('/api/tournament/{id}/players',  resources.TournamentPlayers())
api.add_route('/api/tournament/{id}/teams',  resources.TournamentTeams())
api.add_route('/api/tournament/{id}/matches',  resources.TournamentMatches())
api.add_route('/api/tournament/{id}/spirits',  resources.Spirits())
api.add_route('/api/tournament/{id}/missing-spirits',  resources.MissingSpirits())

api.add_route('/api/match/{id}',  resources.Match(m.Match))
api.add_route('/api/match/{id}/points',  resources.MatchPoints())
api.add_route('/api/match/{id}/point/{order}',  resources.MatchPoint())
api.add_route('/api/match/{id}/spirits',  resources.Spirit())

api.add_route("/api/users", resources.Users())
api.add_route("/api/user/{id}", resources.User())

api.add_route("/api/login", resources.Login())
api.add_route("/api/forgotten-password", resources.ForgottenPassword())

# not implemented
api.add_route('/api/tournament/{id}/groups',  resources.TournamentGroups())

# errors
# TODO: doplnit
api.add_error_handler(RuntimeError, errors.InternalServerError)
api.add_error_handler(TypeError, errors.BadRequest)
api.add_error_handler(KeyError, errors.BadRequest)
api.add_error_handler(ValueError, errors.BadRequest)
api.add_error_handler(AttributeError, errors.BadRequest)
api.add_error_handler(pw.IntegrityError, errors.BadRequest)
api.add_error_handler(m.Club.DoesNotExist, errors.NotFound)
api.add_error_handler(m.User.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Player.DoesNotExist, errors.NotFound)
# api.add_error_handler(m.ClubHasPlayer.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Division.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Team.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Tournament.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Field.DoesNotExist, errors.NotFound)
api.add_error_handler(m.TeamAtTournament.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Identificator.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Match.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Standing.DoesNotExist, errors.NotFound)
api.add_error_handler(m.PlayerAtTournament.DoesNotExist, errors.NotFound)
# api.add_error_handler(m.Spirit.DoesNotExist, errors.NotFound)
# api.add_error_handler(m.SpiritAvg.DoesNotExist, errors.NotFound)