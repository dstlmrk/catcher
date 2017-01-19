# from catcher.api.privileges import HasRole
# from catcher import models
# import falcon

from falcon import HTTP_201, HTTP_204, HTTP_404
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

    # @falcon.before(HasRole(["admin"]))
    # TODO: pouze admin
    def on_delete(self, req, resp, id):
        resp.status = HTTP_204 if models.Team.delete(int(id)) else HTTP_404


class Teams():

    def on_get(self, req, resp):
        # TODO: parametrizovat dotaz pro specifictejsi vyber?
        req.context['result'] = {
            'teams': [team.to_dict() for team in models.Team.get_teams()]
        }

    def on_post(self, req, resp):
        # TODO: pozor na opravneni, tym zatim muze vytvorit jenom admin
        user = models.Team.create(**req.context['data']).to_dict()
        resp.status = HTTP_201
        req.context['result'] = user
