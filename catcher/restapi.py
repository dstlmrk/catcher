#!/usr/bin/python
# coding=utf-8

import falcon
from api import errors
from api import middleware
import resources as r
import models as m
import peewee as pw

import logger


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



# # informace o konkretnim turnaji
# api.add_route('/api/tournament/{id}', r.Tournament(m.Tournament, []))
# vytvori kompletni turnaj
# api.add_route('/api/tournaments/create', r.CreateTournament())
# ativuje turnaj
# api.add_route('/api/tournament/{id}/active', r.ActiveTournament())
# # u aktivnich nebo jiz skoncenych turnaju vrati poradi na turnaji
# api.add_route('/api/tournament/{id}/standings', r.TournamentStandings())
# # vrati seznam tymu na turnaji
# api.add_route('/api/tournament/{id}/teams', r.TournamentTeams())
# # vrati seznam hracu v tymu
# api.add_route('/api/tournament/{id}/teams/players', r.TournamentTeamsAndPlayers())
# # vrati seznam hracu v tymu
# api.add_route('/api/tournament/{id}/team/{teamId}/players', r.TournamentTeamAndPlayers())
# # vrati seznam hracu na turnaji
# api.add_route('/api/tournament/{id}/players', r.TournamentPlayers())
# # vrati seznam zapasu na turnaji
# api.add_route('/api/tournament/{id}/matches', r.TournamentMatches())
# # vrati seznam zapasu na turnaji
# api.add_route('/api/tournament/{id}/match/{matchId}', r.TournamentMatch())
# # slouzi pro pridavani hracu do soupisky
# api.add_route('/api/tournament/{id}/rosters/', r.Rosters())

# # informace o zapase
# api.add_route('/api/match/{id}', r.Match(m.Match,[]))
# # ukonci zapas (TODO: spocitaji se celkove statistiky hracu)
# api.add_route('/api/match/{id}/terminate', r.TerminateMatch)
# # seznam vsech zapasu
# api.add_route('/api/matches', r.Matches(m.Match))

# # TODO: zkusit dovymyslet ostatni api

# # vytvori v zapase novy bod, automaticky spocita aktualni skore - GET, POST
# api.add_route('/api/match/{id}/points', None) # parametrem muze byt asistujici a skorujici
# # upravi bod, PUT, DELETE (musi se vymyslet order)
# api.add_route('/api/match/{id}/point/{order}', None)

# # zadat spirit
# api.add_route('/api/match/{id}/spirit', None)

# ukonci turnaj a zverejni celkove statistiky spiritu

# errors
api.add_error_handler(Exception, errors.InternalServerError)
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