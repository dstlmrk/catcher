#!/usr/bin/python
# coding=utf-8

from api.resource import Collection
import falcon

class Divisions(Collection):
    
    def on_post(self, req, resp):
    	# method not allowed
    	resp.status = falcon.HTTP_405