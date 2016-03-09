#!/usr/bin/python
# coding=utf-8

import falcon
import simplejson as json

class Authorization(object):
    def process_request(self, req, resp):
        pass

# -----------TODO --------------------------------------------------
# class AuthMiddleware(object):

#     def process_request(self, req, resp):
#         token = req.get_header('X-Auth-Token')
#         project = req.get_header('X-Project-ID')

#         if token is None:
#             description = ('Please provide an auth token '
#                            'as part of the request.')

#             raise falcon.HTTPUnauthorized('Auth token required',
#                                           description,
#                                           href='http://docs.example.com/auth')

#         if not self._token_is_valid(token, project):
#             description = ('The provided auth token is not valid. '
#                            'Please request a new token and try again.')

#             raise falcon.HTTPUnauthorized('Authentication required',
#                                           description,
#                                           href='http://docs.example.com/auth',
#                                           scheme='Token; UUID')

#     def _token_is_valid(self, token, project):
#         return True  # Suuuuuure it's valid...
# ------------------------------------------------------------------

class RequireJSON(object):
    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')

class JSONTranslator(object):
    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body
        if req.content_length in (None, 0):
            return # nothing to do

        body = req.stream.read()

        if not body:
            raise falcon.HTTPBadRequest(
                'Empty request body',
                'A valid JSON document is required.'
                )
        
        try:
            req.context['data'] = json.loads(body)
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                'Malformed JSON',
                'Could not decode the request body. The '
                'JSON was incorrect or not encoded as '
                'UTF-8.'
                )

    def process_response(self, req, resp, resource):
        # TODO: v pripade souboru to muze fungovat jinak, musi se kdyztak pouzit
        # reseni z dokumentace
        if resp.body is not None:
            resp.body = json.dumps(resp.body)
