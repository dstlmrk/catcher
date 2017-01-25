import falcon
from falcon import HTTP_201, HTTP_204, HTTP_404
from catcher import models
from catcher.api.privileges import HasRole, IsOwner, OrPrivilege


class Team(object):

    def on_get(self, req, resp, id):
        """Get team"""
        session = req.context['session']
        req.context['result'] = models.Team.get(session, int(id)).to_dict()

    @falcon.before(OrPrivilege(HasRole(["admin"]), IsOwner(models.Team)))
    def on_put(self, req, resp, id):
        """Edit team"""
        session = req.context['session']
        req.context['result'] = models.Team.edit(
            session, id=int(id), **req.context['data']
        )

    @falcon.before(HasRole(["admin"]))
    def on_delete(self, req, resp, id):
        """Delete team (set delete flag)"""
        session = req.context['session']
        resp.status = HTTP_204 if models.Team.delete(session, int(id)) else HTTP_404


class Teams(object):

    def on_get(self, req, resp):
        """Get all teams"""
        session = req.context['session']
        # TODO: moznost parametrizovat
        req.context['result'] = {
            'teams': [team.to_dict() for team in models.Team.get_all(session)]
        }

    @falcon.before(HasRole(["admin"]))
    def on_post(self, req, resp):
        """Create new team"""
        session = req.context['session']
        user = models.Team.create(session, **req.context['data']).to_dict()
        resp.status = HTTP_201
        req.context['result'] = user
