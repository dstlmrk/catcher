#!/usr/bin/python
# coding=utf-8

from catcher.resource import Collection, Item

class Team(Item):
    def on_get(self, req, resp, id):
        super(Team, self).on_get(req, resp, id)

        clubName = req.context['result']['club']['name']
        degree = req.context['result']['degree']
        name = req.context['result']['club']['name']
        teamName = clubName + " " + degree
        
	req.context['result']['name'] = teamName

class Teams(Collection):
    pass