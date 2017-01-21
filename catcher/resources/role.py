from catcher import models


class Roles():

    def on_get(self, req, resp):
        req.context['result'] = {
            'roles': [role.to_dict() for role in models.Role.get_all()]
        }
