import falcon
from falcon import HTTP_201, HTTP_204, HTTP_404
from catcher import models
from catcher.api.privileges import HasRole, IsOwner, OrPrivilege


class Team(object):

    def on_get(self, req, resp, id):
        """Get team"""
        req.context['result'] = models.Team.get(id=int(id)).to_dict()

    @falcon.before(OrPrivilege(HasRole(["admin"]), IsOwner(models.Team)))
    def on_put(self, req, resp, id):
        """Edit team"""
        req.context['result'] = models.Team.edit(
            id=int(id), **req.context['data']
        )

    @falcon.before(HasRole(["admin"]))
    def on_delete(self, req, resp, id):
        """Delete team (set delete flag)"""
        resp.status = HTTP_204 if models.Team.delete(int(id)) else HTTP_404


class Teams(object):

    def on_get(self, req, resp):
        """Get all teams"""
        # TODO: moznost parametrizovat
        req.context['result'] = {
            'teams': [team.to_dict() for team in models.Team.get_all()]
        }

    @falcon.before(HasRole(["admin"]))
    def on_post(self, req, resp):
        """Create new team"""
        user = models.Team.create(**req.context['data']).to_dict()
        resp.status = HTTP_201
        req.context['result'] = user
