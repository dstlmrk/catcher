# #!/usr/bin/python
# # coding=utf-8
#
import falcon
import ujson
import json
# from catcher import models
import datetime
# from playhouse.shortcuts import model_to_dict
# import logging
# from catcher.models import User, NullUser
from catcher.logger import logger
logger.setLevel('DEBUG')
from catcher.models.base import Base


# TODO: sjednotit json, ujson, simplejson atd.

class Crossdomain(object):
    def process_request(self, req, resp):
        resp.append_header(
            "Access-Control-Allow-Origin", "*"
        )
        resp.append_header(
            "Access-Control-Allow-Headers",
            "Content-Type,Authorization,X-Name"
        )
        resp.append_header(
            "Access-Control-Allow-Methods",
            "PUT,POST,DELETE,GET"
        )


class Authorization(object):
    def process_request(self, req, resp):
        pass

        # user = NullUser()
        # try:
        #     if req.auth:
        #         user = User.get(api_key=req.auth)
        # except User.DoesNotExist:
        #     pass
        #
        # # debug
        # print("LOGGED: %s" % user)
        #
        # req.context["user"] = user


class RequireJSON(object):
    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.'
            )

        if req.method in ('POST', 'PUT'):
            if not req.content_type or 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.'
                )


class JSONTranslator(object):
    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body
        if req.content_length in (None, 0):
            return  # nothing to do

        body = req.stream.read()

        if not body:
            raise falcon.HTTPBadRequest(
                'Empty request body',
                'A valid JSON document is required.'
            )

        try:
            req.context['data'] = ujson.loads(body)
            # TODO: logovani pro develop
            logger.warn(req.method + " " + req.uri + " " + str(req.context['data']))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPBadRequest(
                'Malformed JSON',
                'Could not decode the request body. The '
                'JSON was incorrect or not encoded as '
                'UTF-8.'
            )

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return
        resp.body = json.dumps(
            req.context['result'],
            default=JSONTranslator.converter
        )

    @staticmethod
    def converter(obj):
        """
        JSON serializer for objects not serializable by default json code.
        """
        if (isinstance(obj, datetime.time)
            or isinstance(obj, datetime.date)
            or isinstance(obj, datetime.datetime)
            ):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Base):
            return obj.to_dict()
        logger.error(
            "Converter doesn't know how convert data (%s [%s])" % (
                obj, type(obj))
        )
        raise TypeError("Type not serializable")
