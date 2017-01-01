#

from falcon import HTTP_201
from catcher import models


class User():

    def on_get(self, req, resp, id):
        req.context['result'] = models.User.get(id=int(id)).to_dict()

    # @falcon.before(IsThatUser())
    def on_put(self, req, resp, id):
        req.context['result'] = models.User.edit(id=int(id), **req.context['data'])

class Users():

    def on_get(self, req, resp):
        # TODO: parametrizovat dotaz pro specifictejsi vyber?
        req.context['result'] = {
            'users': [user.to_dict() for user in models.User.get_users()]
        }

    def on_post(self, req, resp):
        # TODO: pozor na opravneni, admina muze vytvorit jenom admin atd.
        user = models.User.create(**req.context['data']).to_dict()
        resp.status = HTTP_201
        req.context['result'] = user

    # TODO: spis doladit opravneni, nez to, ze se vyhazuje spravna vyjimka a uzivatel vidi spravnou chybu
