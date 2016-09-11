#!/usr/bin/python
# coding=utf-8

# from catcher.api.resource import Collection, Item
# from playhouse.shortcuts import model_to_dict
# from catcher import models as m
# from catcher.api.privileges import Privilege
from catcher import models
# import falcon


def get_valid_expressions(expressions):
    return [exp for exp in expressions if exp.rhs is not None]


class Team(object):

    def on_get(self, req, resp, id):
        req.context['result'] = models.Team.get(id=int(id))

class Teams(object):

    def on_get(self, req, resp):
        exps = get_valid_expressions([
            models.Team.city == req.get_param("city"),
            models.Team.country == req.get_param("country"),
            models.Team.division == req.get_param_as_int("division_id")
        ])
        select_teams = models.Team.select()
        if exps:
            select_teams = select_teams.where(*exps)
        teams = [team for team in select_teams]
        req.context['result'] = {'teams': teams}
        
# class Team(Item):
    
#     # @falcon.before(Privilege(["club", "admin"]))
#     def on_put(self, req, resp, id):
#         Privilege.checkClub(req.context['user'], m.Team.get(id=id).clubId)
#         super(Team, self).on_put(req, resp, id, ['divisionId', 'degree'])
    
#     def on_get(self, req, resp, id):
#         req.context['result'] = Teams.getTeams(id)[0]

#     # @falcon.before(Privilege(["admin"]))
#     def on_delete(self, req, resp, id):
#         super(Team, self).on_delete(req, resp, id)

# class Teams(Collection):

#     @staticmethod
#     def getTeams(teamId = None):
#         whereTeam = "" if teamId is None else (" WHERE team.id = %s" % teamId)
#         q = ("SELECT team.id, team.degree, team.division_id, club.name," +
#              " team.club_id FROM team JOIN club ON club.id = team.club_id %s"
#              % (whereTeam))
#         qr = m.db.execute_sql(q)
#         teams = []
#         for row in qr:
#             teams.append({
#                 'id'         : row[0],
#                 'degree'     : row[1],
#                 'divisionId' : row[2],
#                 'name'       : (row[3] + " " + row[1]),
#                 'clubId'     : row[4]
#                 })
#         return teams
    
#     def on_get(self, req, resp):
#         teams = Teams.getTeams()
#         collection = {
#             'count' : len(teams),
#             'items' : teams
#         }
#         req.context['result'] = collection

#     # @falcon.before(Privilege(["club", "admin"]))
#     def on_post(self, req, resp):
#         Privilege.checkClub(req.context['user'], req.context['data'].get('clubId'))
#         super(Teams, self).on_post(req, resp)