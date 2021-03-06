#!/usr/bin/python
# coding=utf-8

import falcon

class Item(object):
    def __init__(self, model):
        self.model = model

    def on_get(self, req, resp, id):
        item = self.model.get(id=id)
        req.context['result'] = item

    def on_put(self, req, resp, id, editableCols=None):
        data = req.context['data']
        params = None
        if editableCols is not None:
            params = { key : data[key] for key in data if key in editableCols}
        qr = None
        if params:
            qr = self.model.update(**params).where(self.model.id==id).execute()
        req.context['result'] = self.model.select().where(self.model.id==id).get()
        resp.status = falcon.HTTP_200 if qr else falcon.HTTP_304

    def on_delete(self, req, resp, id):
        self.model.delete().where(self.model.id==id).execute()

class Collection(object):
    def __init__(self, model):
        self.model = model

    def on_get(self, req, resp):
        qr = self.model.select()
        # .dicts()
        items = [item for item in qr]
        collection = {
            'count' : len(items),
            'items' : items
        }
        req.context['result'] = collection

    def on_post(self, req, resp):
        data = req.context['data']
        item = self.model.create(**data)
        req.context['result'] = item
        resp.status = falcon.HTTP_201