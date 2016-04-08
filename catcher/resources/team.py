#!/usr/bin/python
# coding=utf-8

from api.resource import Collection, Item
from playhouse.shortcuts import model_to_dict
import models as m

class Team(Item):
    
    def on_put(self, req, resp, id):
        super(Team, self).on_put(req, resp, id, ['divisionId', 'degree'])
    
    def on_get(self, req, resp, id):
        qr = self.model.select().where(self.model.id==id).get()
        team = {
            'id'    : qr.id,
            'degree': qr.degree,
            'clubId': qr.club_id,
            'name'  : qr.name,
            'division' : qr.division
        }
        req.context['result'] = team

class Teams(Collection):
    
    def on_get(self, req, resp):
        q = ("SELECT team.id, team.degree, team.division_id, club.name," +
             " team.club_id FROM catcher.team JOIN club ON club.id = team.club_id")
        qr = m.db.execute_sql(q)
        teams = []
        for row in qr:
            teams.append({
                'id'         : row[0],
                'degree'     : row[1],
                'divisionId' : row[2],
                'name'       : (row[3] + " " + row[1]),
                'clubId'     : row[4]
                })

        collection = {
            'count'   : len(teams),
            'teams' : teams
        }

        req.context['result'] = collection

    def on_post(self, req, resp):
        req.context['data']['division'] = req.context['data']['divisionId']
        del req.context['data']['divisionId']
        req.context['data']['club'] = req.context['data']['clubId']
        del req.context['data']['clubId']
        super(Teams, self).on_post(req, resp)
