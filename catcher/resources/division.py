from catcher import models


class Divisions():

    def on_get(self, req, resp):
        """Get all divisions"""
        session = req.context['session']
        req.context['result'] = {
            'divisions': [
                division.to_dict() for division in models.Division.get_all(
                    session
                )
            ]
        }
