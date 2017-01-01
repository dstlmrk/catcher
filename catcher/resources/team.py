# from catcher.api.privileges import HasRole
# from catcher import models
# import falcon

from catcher import models

# def get_valid_expressions(expressions):
#     return [exp for exp in expressions if exp.rhs is not None]


class Team():

    def on_get(self, req, resp, id):
        req.context['result'] = models.Team.get(id=int(id)).to_dict()


    # # TODO: pridat opravneni pouze pro majitele tymu nebo admina
    # def on_put(self, req, resp, id):
    #     team = models.Team.get(id=int(id))
    #     team.set_attributes(**req.context['data'])
    #     team.save()
    #     req.context['result'] = team
    #
    # @falcon.before(HasRole(["admin"]))
    # def on_delete(self, req, resp, id):
    #     # TODO: mazani by melo probihat jenom jako (kvuli statistikam apod.)
    #     models.Team.delete().where(models.Team.id == int(id)).execute()


class Teams():
    pass
# class Teams(object):
#
#     def on_get(self, req, resp):
#         exps = get_valid_expressions([
#             models.Team.city == req.get_param("city"),
#             models.Team.country == req.get_param("country"),
#             models.Team.division == req.get_param_as_int("division_id")
#         ])
#         select_teams = models.Team.select()
#         if exps:
#             select_teams = select_teams.where(*exps)
#         teams = [team for team in select_teams]
#         req.context['result'] = {'teams': teams}
#
#     def on_post(self, req, resp):
#         post = req.context['data']
#         req.context['result'] = models.Team.create(**post)
#         resp.status = falcon.HTTP_201
