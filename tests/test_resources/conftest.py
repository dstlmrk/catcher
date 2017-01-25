from falcon import testing
from catcher.restapi import api
from catcher.models import User
import pytest


@pytest.fixture(scope='module')
def client():
    return testing.TestClient(api)


@pytest.fixture(scope='function')
def headers_with_auth(session, users):
    user, api_key, valid_to = User.log_in(session, "admin_login", "admin_password")
    return {'Content-Type': 'application/json', 'Authorization': api_key}


@pytest.fixture(scope='session')
def headers():
    return {'Content-Type': 'application/json'}
