from catcher.models import Division


def test_api_divisions_get(client, session):
    divisions_count = session.query(Division).count()
    result = client.simulate_get('/api/divisions')
    assert len(result.json['divisions']) == divisions_count
