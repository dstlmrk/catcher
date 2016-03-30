#!/usr/bin/python
# coding=utf-8

from api.resource import Collection, Item
import models as m

class TerminateMatch(object):

    def on_put(self, req, resp, id):
        m.Match.\
            update(terminated = True).\
            where(m.Match.id == id).\
            execute()
        editedMatch = m.Match.get(id=id)
        req.context['result'] = editedMatch

class Match(Item):
    pass

class Matches(Collection):
    pass