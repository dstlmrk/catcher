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


def test_api_team_put(client, headers_with_admin_auth, teams):
    team = {
        'city': 'Brno', 'id': 1, 'shortcut': 'BRN', 'name': 'FC Prague',
        'country': 'CZE', 'division_id': 2, 'deleted': False,
        'user_id': None, 'cald_id': None
    }
    result = client.simulate_put(
        '/api/team/1',
        headers=headers_with_admin_auth,
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


def test_api_team_delete(client, session, headers_with_admin_auth, teams):
    result = client.simulate_delete(
        '/api/team/1',
        headers=headers_with_admin_auth
    )
    assert result.status_code == 204
    assert session.query(Team).get(1).deleted == True


def test_api_teams_get(client, teams, session):
    teams_count = session.query(Team).count()
    result = client.simulate_get('/api/teams')
    assert len(result.json['teams']) == teams_count


def test_api_teams_post(client, headers_with_admin_auth, session):
    teams_count = session.query(Team).count()
    session.commit()
    team = {
        'city': 'Brno', 'shortcut': 'BRN', 'name': 'FC Prague',
        'country': 'CZE', 'division_id': 2
    }
    result = client.simulate_post(
        '/api/teams',
        headers=headers_with_admin_auth,
        body=json.dumps(team)
    )
    assert result.status_code == 201
    assert result.json['name'] == session.query(Team).get(result.json['id']).name
    assert teams_count + 1 == session.query(Team).count()
