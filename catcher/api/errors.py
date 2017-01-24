import falcon
import traceback


def not_found(ex, req, resp, params):
    raise falcon.HTTPNotFound()


def bad_request(ex, req, resp, params):
    traceback.print_exc()
    raise falcon.HTTPBadRequest(ex.__class__.__name__, str(ex))


def internal_server_error(ex, req, resp, params):
    if isinstance(ex, falcon.HTTPError):
        raise
    traceback.print_exc()
    raise falcon.HTTPInternalServerError(ex.__class__.__name__, str(ex))
