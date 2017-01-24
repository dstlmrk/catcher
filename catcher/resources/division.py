from catcher import models


class Divisions():

    def on_get(self, req, resp):
        """Get all divisions"""
        req.context['result'] = {
            'divisions': [
                division.to_dict() for division in models.Division.get_all()
            ]
        }
