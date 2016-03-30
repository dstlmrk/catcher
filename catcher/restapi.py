#!/usr/bin/python
# coding=utf-8

import falcon
from api import errors
from api import middleware
import resources as r
import models as m

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

# informace o konkretnim turnaji
api.add_route('/api/tournament/{tournamentId}', r.Tournament(m.Tournament, []))
# seznam vsech turnaju
api.add_route('/api/tournaments', r.Tournaments(m.Tournament))
# vytvori kompletni turnaj
api.add_route('/api/tournaments/create', r.CreateTournament())
# ativuje turnaj
api.add_route('/api/tournament/{tournamentId}/active', r.ActiveTournament())
# u aktivnich nebo jiz skoncenych turnaju vrati poradi na turnaji
api.add_route('/api/tournament/{tournamentId}/standings', r.Standings())
# vrati seznam tymu na turnaji
# TODO: asi bych mohl vracet vcetne soupisek
api.add_route('/api/tournament/{tournamentId}/teams', r.TeamsAtTournament())
# informace o zapase
api.add_route('/api/match/{id}', r.Match(m.Match,[]))
# ukonci zapas
api.add_route('/api/match/{id}/terminate', r.TerminateMatch)
# seznam vsech zapasu
api.add_route('/api/matches', r.Matches(m.Match))

# manipulace s hracem na turnaji
api.add_route('/api/tournament/{tournamentId}/team/{teamId}/player/{playerId}', r.PlayerAtTournament())

# errors
api.add_error_handler(Exception, errors.InternalServerError)
api.add_error_handler(TypeError, errors.BadRequest)
api.add_error_handler(KeyError, errors.BadRequest)
api.add_error_handler(ValueError, errors.BadRequest)
api.add_error_handler(AttributeError, errors.BadRequest)
api.add_error_handler(m.Club.DoesNotExist, errors.NotFound)
api.add_error_handler(m.User.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Player.DoesNotExist, errors.NotFound)
api.add_error_handler(m.ClubHasPlayer.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Division.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Team.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Tournament.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Field.DoesNotExist, errors.NotFound)
api.add_error_handler(m.TeamAtTournament.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Identificator.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Match.DoesNotExist, errors.NotFound)
api.add_error_handler(m.Standing.DoesNotExist, errors.NotFound)
api.add_error_handler(m.PlayerAtTournament.DoesNotExist, errors.NotFound)