#!/usr/bin/python
# coding=utf-8

from api.resource import Collection, Item

class Team(Item):
    pass
    # def on_get(self, req, resp, id):
        # super(Team, self).on_get(req, resp, id)
        # req.context['result'] = Team.appendTeamName(req.context['result']

class Teams(Collection):
    pass