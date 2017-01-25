from catcher.models import Team
import json

def test_api_team_get(client, teams):
    team = {
        'city': 'Prague', 'id': 1, 'shortcut': 'FCP', 'name': 'FC Prague',
        'country': 'CZE', 'division_id': 1, 'deleted': False,
        'user_id': None, 'cald_id': None
    }
    result = client.simulate_get('/api/team/1')
    assert result.json == team


def test_api_team_put(client, headers_with_auth, teams):
    team = {
        'city': 'Brno', 'id': 1, 'shortcut': 'BRN', 'name': 'FC Prague',
        'country': 'CZE', 'division_id': 2, 'deleted': False,
        'user_id': None, 'cald_id': None
    }
    result = client.simulate_put(
        '/api/team/1',
        headers=headers_with_auth,
        body=json.dumps({
            'city': 'Brno',
            'shortcut': 'BRN',
            'division_id': 2
        })
    )
    assert result.status_code == 200
    assert result.json == team


def test_api_team_put_unauthorized(client, headers):
    result = client.simulate_put(
        '/api/team/1',
        headers=headers,
        body=json.dumps({'city': 'Brno'})
    )
    assert result.status_code == 401
    assert result.json['title'] == 'Authentication Required'


# TODO: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# TODO: tady pokracuju

def test_api_team_delete(client, teams):
    pass




# http://falcon.readthedocs.io/en/stable/api/testing.html

def test_api_teams_get(client, teams, session):
    teams_count = session.query(Team).count()
    result = client.simulate_get('/api/teams')
    assert len(result.json['teams']) == teams_count

