#!/usr/bin/python
# coding=utf-8

import falcon
import traceback
import logging

def cutQuotationMark(ex):
	return ex.replace("\"","")

def NotFound(ex, req, resp, params):
	raise falcon.HTTPNotFound(
		title       = "Not Found",
		description = "Instance matching query does not exist"
		)

def BadRequest(ex, req, resp, params):
	traceback.print_exc()
	raise falcon.HTTPBadRequest(
		ex.__class__.__name__,
		cutQuotationMark(str(ex))
		)

def InternalServerError(ex, req, resp, params):
	logging.error(ex)
	if isinstance(ex, falcon.HTTPError):
		raise
	traceback.print_exc()
	raise falcon.HTTPInternalServerError(
		ex.__class__.__name__,
		cutQuotationMark(str(ex))
		)
