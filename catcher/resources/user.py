from falcon import HTTP_201, HTTP_204, HTTP_404
from catcher import models
from catcher.api.privileges import HasRole, OrPrivilege, IsThatUser
import falcon


class User():

    def on_get(self, req, resp, id):
        """Get user"""
        req.context['result'] = models.User.get(id=int(id)).to_dict()

    @falcon.before(OrPrivilege(HasRole(["admin"]), IsThatUser()))
    def on_put(self, req, resp, id):
        """Edit user"""
        # TODO: obyc uzivatel nesmi upravovat role_id a login
        # TODO: pridat moznost, aby uzivatel mohl zmenit heslo (ale musel se zaroven prokazat tim starym)
        req.context['result'] = models.User.edit(id=int(id), **req.context['data'])

    @falcon.before(HasRole(["admin"]))
    def on_delete(self, req, resp, id):
        """Delete user (hard-delete!)"""
        resp.status = HTTP_204 if models.User.delete(int(id)) else HTTP_404

class Users():

    def on_get(self, req, resp):
        """Get all users"""
        # TODO: moznost parametrizovat
        req.context['result'] = {
            'users': [user.to_dict() for user in models.User.get_all()]
        }

    @falcon.before(HasRole(["admin"]))
    def on_post(self, req, resp):
        """Create new user (this api is for admins that manually add new users)"""
        user = models.User.create(**req.context['data']).to_dict()
        resp.status = HTTP_201
        req.context['result'] = user
