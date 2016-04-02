#!/usr/bin/python
# coding=utf-8

from playhouse.shortcuts import model_to_dict

class Item(object):
    def __init__(self, model, editableCols):
        self.model = model
        self.editableCols = editableCols

    def on_get(self, req, resp, id):
        item = self.model.select().where(self.model.id==id).get()
        # TODO: napsat na to nejakou obecnou metodu/funkci, pouzije se i v kolekci
        itemDict = model_to_dict(item)
        if 'additionalList' in req.params:
            param = req.params['additionalList']
            try:
                exec("additionalList = item.%s" % (param))
            except Exception, e:
                raise Exception("Bad params in additionalList")
            subitems = []
            for subitem in additionalList:
                print model_to_dict(subitem)
                # TODO: vyuziva __str__ s privatni metodou!
                subitems.append(model_to_dict(subitem))
            itemDict[param] = subitems
        
        req.context['result'] = itemDict

    def on_put(self, req, resp, id):
        requestJson = req.context['data']
        params = { key : requestJson[key] for key in requestJson if key in self.editableCols}
        qr = self.model.update(**params).where(self.model.id==id).execute()
        req.context['result'] = self.model.select().where(self.model.id==id).dicts().get()
        resp.status = falcon.HTTP_201 if qr else falcon.HTTP_304

    def on_delete(self, req, resp, id):
        self.model.delete().where(self.model.id==id).execute()

class Collection(object):
    def __init__(self, model):
        self.model = model

    def on_get(self, req, resp):
        qr = self.model.select().dicts()
        items = [item for item in qr]
        collection = {
            'count' : len(items),
            'items' : items
        }
        req.context['result'] = collection

    def on_post(self, req, resp):
        requestJson = req.context['data']
        item = self.model.create(**requestJson)
        req.context['result'] = item