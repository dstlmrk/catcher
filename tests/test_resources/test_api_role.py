from catcher.models import Role


def test_api_roles_get(client, session):
    roles_count = session.query(Role).count()
    result = client.simulate_get('/api/roles')
    assert len(result.json['roles']) == roles_count
