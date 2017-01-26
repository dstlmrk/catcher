from catcher.models import User
import json
import pytest


def test_api_user_get(client, users):
    user = {
        'id': 1, 'login': 'user1', 'email': 'user1@test.cz', 'role_id': 1
    }
    result = client.simulate_get('/api/user/1')
    assert result.json['id'] == user['id']
    assert result.json['email'] == user['email']


def test_api_user_get_password(client, users):
    result = client.simulate_get('/api/user/1')
    with pytest.raises(KeyError):
        result.json['password']


@pytest.mark.parametrize("body", [
    {'email': 'new@email.cz'},
    {'password': 'new_password', 'old_password': 'password1'}
])
def test_api_user_put(client, headers_with_user_auth, users, body):
    result = client.simulate_put(
        '/api/user/1',
        headers=headers_with_user_auth,
        body=json.dumps(body)
    )
    assert result.status_code == 200
    if body.get('email'):
        assert result.json['email'] == body['email']


@pytest.mark.parametrize("body", [{'password': 'new_password'}, {'login': 'new_login'}, {'role_id': 2}])
def test_api_user_put_unauthorized(client, headers, body):
    result = client.simulate_put(
        '/api/user/1',
        headers=headers,
        body=json.dumps(body)
    )
    assert result.status_code == 401
    assert result.json['title'] == 'Authentication Required'


def test_api_user_put_password_change(client, headers_with_admin_auth):
    result = client.simulate_put(
        '/api/user/1',
        headers=headers_with_admin_auth,
        body=json.dumps({'password': 'new_password'})
    )
    assert result.status_code == 401
    assert result.json['title'] == 'Authentication Required'


def test_api_user_delete(client, session, headers_with_admin_auth, users):
    users_count = session.query(User).count()
    session.commit()
    result = client.simulate_delete(
        '/api/user/1',
        headers=headers_with_admin_auth
    )
    assert result.status_code == 204
    assert users_count == session.query(User).count() + 1


def test_api_user_delete_unauthorized(client, session, headers, users):
    result = client.simulate_delete(
        '/api/user/1',
        headers=headers
    )
    assert result.status_code == 401
    assert result.json['title'] == 'Authentication Required'


def test_api_users_get(client, users, session):
    users_count = session.query(User).count()
    result = client.simulate_get('/api/users')
    assert len(result.json['users']) == users_count


def test_api_users_post(client, headers_with_admin_auth, session):
    users_count = session.query(User).count()
    session.commit()
    user = {
        'login': 'user8', 'email': 'user8@test.cz', 'role_id': 1, 'password': 'password8'
    }
    result = client.simulate_post(
        '/api/users',
        headers=headers_with_admin_auth,
        body=json.dumps(user)
    )
    assert result.status_code == 201
    assert result.json['email'] == session.query(User).get(result.json['id']).email
    assert users_count + 1 == session.query(User).count()
