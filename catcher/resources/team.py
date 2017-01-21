import falcon
from falcon import HTTP_201, HTTP_204, HTTP_404
from catcher import models
from catcher.api.privileges import HasRole


class Team():

    def on_get(self, req, resp, id):
        req.context['result'] = models.Team.get(id=int(id)).to_dict()


    # TODO: pridat opravneni pouze pro majitele tymu nebo admina
    def on_put(self, req, resp, id):
        req.context['result'] = models.Team.edit(id=int(id), **req.context['data'])

    # @falcon.before(HasRole(["admin"]))
    def on_delete(self, req, resp, id):
        resp.status = HTTP_204 if models.Team.delete(int(id)) else HTTP_404


class Teams():

    def on_get(self, req, resp):
        # TODO: parametrizovat dotaz pro specifictejsi vyber?
        req.context['result'] = {
            'teams': [team.to_dict() for team in models.Team.get_all()]
        }

    def on_post(self, req, resp):
        # TODO: pozor na opravneni, tym zatim muze vytvorit jenom admin
        user = models.Team.create(**req.context['data']).to_dict()
        resp.status = HTTP_201
        req.context['result'] = user
