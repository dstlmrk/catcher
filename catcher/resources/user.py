#!/usr/bin/python
# coding=utf-8

from catcher import models
from peewee import prefetch
from catcher.api.privileges import HasRole, IsThatUser
import falcon


class Users(object):

    @falcon.before(HasRole(["admin"]))
    def on_get(self, req, resp):
        users_with_roles = prefetch(
            models.User.select(),
            models.Role.select()
        )
        users = []
        for user in users_with_roles:
            user.password = user.api_key = None
            users.append(user)
        req.context['result'] = {'users': users}

    def on_post(self, req, resp):
        '''registration'''
        post = req.context['data']
        # TODO: pozor na opravneni, admina muze vytvorit jenom admin atd.
        # zatim je mozno vytvorit pouze organizatora
        user = models.User.create(**post)
        if not post.get('test'):
            models.Login.send_init_password(user)
        resp.status = falcon.HTTP_201


class User(object):

    @falcon.before(IsThatUser())
    def on_put(self, req, resp):
        '''edit user data and set new password'''
        user = models.User.get(id=req.get_param_as_int("id", True))
        data = req.context['data']

        # TODO: mel bych poslat zpravu na novy email
        user.substituteEmail(data.get('email'))
        user.substitutePassword(
            data.get('old_password'),
            data.get('new_password')
        )
        user.save()
        user.password = user.api_key = None
        req.context['result'] = user

    def on_get(self, req, resp):
        user = models.User.get(id=req.get_param_as_int("id", True))
        user.password = user.api_key = None
        req.context['result'] = user
