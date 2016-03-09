#!/usr/bin/python
# coding=utf-8

import falcon
import traceback

def NotFound(ex, req, resp, params):
	raise falcon.HTTPNotFound()

def BadRequest(ex, req, resp, params):
	traceback.print_exc()
	raise falcon.HTTPBadRequest(ex.__class__.__name__, str(ex))

def InternalServerError(ex, req, resp, params):
	if isinstance(ex, falcon.HTTPError):
		raise
	traceback.print_exc()
	raise falcon.HTTPInternalServerError(ex.__class__.__name__, str(ex))
