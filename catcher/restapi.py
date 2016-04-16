#!/usr/bin/python
# coding=utf-8

import logger
import falcon
from api import errors
from api import middleware
import resources as r
import models as m
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
        # middleware.Authorization(),
        middleware.RequireJSON(),
        middleware.JSONTranslator(),
        ]
    )

# resources are represented by long-lived class instances
# TODO: editable cols presunout nekam, kde je muzu upravovat zaroven i pro testy
api.add_route('/api/club/{id}', r.Club(m.Club))
api.add_route('/api/club/{id}/players', r.ClubPlayers())
api.add_route('/api/club/{id}/teams', r.ClubTeams())
api.add_route('/api/clubs', r.Clubs(m.Club))

api.add_route('/api/player/{id}', r.Player(m.Player))
api.add_route('/api/players', r.Players(m.Player))

api.add_route('/api/divisions', r.Divisions(m.Division))

api.add_route('/api/team/{id}', r.Team(m.Team))
api.add_route('/api/teams', r.Teams(m.Team))

api.add_route('/api/tournaments', r.Tournaments(m.Tournament))
api.add_route('/api/tournament/{id}', r.Tournament(m.Tournament))
api.add_route('/api/tournament/{id}/standings', r.Standings())
api.add_route('/api/tournament/{id}/players', r.TournamentPlayers())
api.add_route('/api/tournament/{id}/teams', r.TournamentTeams())
api.add_route('/api/tournament/{id}/matches', r.TournamentMatches())
api.add_route('/api/tournament/{id}/spirit', r.Spirits())

api.add_route('/api/match/{id}', r.Match(m.Match))
api.add_route('/api/match/{id}/points', r.MatchPoints())
api.add_route('/api/match/{id}/point/{order}', r.MatchPoint())
api.add_route('/api/match/{id}/spirit', r.Spirit())

# not implemented
api.add_route('/api/tournament/{id}/groups', r.TournamentGroups())

# errors
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