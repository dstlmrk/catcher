import json
from catcher.models import ApiKey, Email
import flexmock
import pytest


def test_api_login_post(client, headers, users):
    flexmock(ApiKey, create=('#api_key', '2018-10-05 22:04:14'))
    result = client.simulate_post(
        '/api/login',
        headers=headers,
        body=json.dumps({'login': 'user1', 'password': 'password1'})
    )
    assert result.json['user']['login'] == 'user1'
    assert result.json['api_key'] == '#api_key'
    assert result.json['valid_to'] == '2018-10-05 22:04:14'


def test_api_registration_post(client, headers, database):
    flexmock(Email, _send_email=None)
    result = client.simulate_post(
        '/api/registration',
        headers=headers,
        body=json.dumps({
            'login': 'user99', 'email': 'user99@new.com'
        })
    )
    assert result.status_code == 201


def test_api_registration_post_existing_user(client, headers, users):
    flexmock(Email, _send_email=None)
    result = client.simulate_post(
        '/api/registration',
        headers=headers,
        body=json.dumps({
            'login': 'user1', 'email': 'user99@new.com'
        })
    )
    # TODO: 400 or 409 conflict?
    assert result.status_code == 400


@pytest.mark.skip()
def test_api_reset_password_post():
    pass
