from falcon import HTTP_201, HTTP_204, HTTP_404
from catcher import models
from catcher.api.privileges import HasRole, OrPrivilege, IsThatUser
from sqlalchemy.orm.exc import NoResultFound
import falcon


class User(object):

    def on_get(self, req, resp, id):
        """Get user"""
        session = req.context['session']
        req.context['result'] = models.User.get(session, int(id)).to_dict()

    @falcon.before(OrPrivilege(HasRole(["admin"]), IsThatUser()))
    def on_put(self, req, resp, id):
        """Edit user (admin can change role_id or login only)"""
        # TODO: after email change send confirm email
        data = req.context['data']
        user = req.context['user']
        session = req.context['session']
        if (data.get('role_id') or data.get('login')) and \
           user.role.type != 'admin':
            # only admin can change role_id or login
            User.raise_401()

        if data.get('password'):
            # password is able to change if old password is valid
            try:
                models.User.get_by_credentials(
                    session, user.login, data.get('old_password')
                )
                del data['old_password']
            except NoResultFound:
                User.raise_401()

        req.context['result'] = models.User.edit(session, int(id), **data)

    @falcon.before(HasRole(["admin"]))
    def on_delete(self, req, resp, id):
        """Delete user (hard-delete!)"""
        session = req.context['session']
        resp.status = HTTP_204 if models.User.delete(
            session, int(id)
        ) else HTTP_404

    @staticmethod
    def raise_401():
        raise falcon.HTTPUnauthorized(
            "Authentication Required", (
                "This server could not verify that "
                "you are authorized to access the document requested."
            )
        )


class Users(object):

    def on_get(self, req, resp):
        """Get all users"""
        # TODO: moznost parametrizovat
        session = req.context['session']
        req.context['result'] = {
            'users': [user.to_dict() for user in models.User.get_all(session)]
        }

    @falcon.before(HasRole(["admin"]))
    def on_post(self, req, resp):
        """Create new user (this api is for admins that manually add new users)"""
        session = req.context['session']
        user = models.User.create(session, **req.context['data']).to_dict()
        resp.status = HTTP_201
        req.context['result'] = user
