#!/usr/bin/python
# coding=utf-8

import falcon
from catcher.api import middleware, errors
from catcher import resources
from sqlalchemy.orm.exc import NoResultFound

# falcon.API instance is callable WSGI app
api = falcon.API(
    middleware=[
        middleware.Crossdomain(),
        middleware.SessionMaker(),
        middleware.Authorization(),
        middleware.RequireJSON(),
        middleware.JSONTranslator(),
        ]
    )

# resources are represented by long-lived class instances
api.add_route('/api/team/{id}', resources.Team())
api.add_route('/api/teams', resources.Teams())

api.add_route('/api/user/{id}', resources.User())
api.add_route('/api/users', resources.Users())

api.add_route('/api/login', resources.Login())
api.add_route('/api/registration', resources.Registration())
api.add_route('/api/reset-password', resources.ResetPassword())

api.add_route('/api/divisions', resources.Divisions())
api.add_route('/api/roles', resources.Roles())

# api.add_route('/api/tournaments',  resources.Tournaments(m.Tournament))
# api.add_route('/api/tournament/{id}',  resources.Tournament(m.Tournament))
# api.add_route('/api/tournament/{id}/standings',  resources.Standings())
# api.add_route('/api/tournament/{id}/players',  resources.TournamentPlayers())
# api.add_route('/api/tournament/{id}/teams',  resources.TournamentTeams())
# api.add_route('/api/tournament/{id}/matches',  resources.TournamentMatches())
# api.add_route('/api/tournament/{id}/spirits',  resources.Spirits())
# api.add_route('/api/tournament/{id}/missing-spirits',  resources.MissingSpirits())

# api.add_route('/api/match/{id}',  resources.Match(m.Match))
# api.add_route('/api/match/{id}/points',  resources.MatchPoints())
# api.add_route('/api/match/{id}/point/{order}',  resources.MatchPoint())
# api.add_route('/api/match/{id}/spirits',  resources.Spirit())

# api.add_route("/api/users", resources.Users())
# api.add_route("/api/user/{id}", resources.User())

# api.add_route("/api/login", resources.Login())
# api.add_route("/api/forgotten-password", resources.ForgottenPassword())

# api.add_route('/api/tournament/{id}/groups', resources.TournamentGroups())
# api.add_route('/api/tournament/{id}/group/{ide}', resources.TournamentGroup())


# errors
api.add_error_handler(Exception, errors.internal_server_error)
api.add_error_handler(ValueError, errors.bad_request)
api.add_error_handler(NoResultFound, errors.not_found)
