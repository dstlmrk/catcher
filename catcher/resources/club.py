#!/usr/bin/python
# coding=utf-8

import json
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

import falcon
from catcher import models

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.



class Item(object):
    def __init__(self, model, editableCols):
        self.model = model
        self.editableCols = editableCols

    def on_get(self, req, resp, id):
        try:
            qRes = self.model.select().where(self.model.id==id).dicts().get()
        except models.Club.DoesNotExist as ex:
            raise falcon.HTTPNotFound()
        else:
            resp.body = qRes

    def on_put(self, req, resp, id):
        requestJson = req.context['data']
        params = { key : requestJson[key] for key in requestJson if key in self.editableCols}
        qr = models.Club.update(**params).where(models.Club.id==id).execute()
        resp.body = models.Club.select().where(models.Club.id==id).dicts().get()
        resp.status = falcon.HTTP_201 if qr else falcon.HTTP_304

class Club(Item):
    pass

class Clubs(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        qRes = models.Club.select().dicts()
        clubs = [club for club in qRes]
        result = {
            'count' : len(clubs),
            'clubs' : clubs
        }
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(result)

    def on_post(self, req, resp):
        pass