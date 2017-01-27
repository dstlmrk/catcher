import os
import sys
# Ondra's tip for _pytest.config.ConftestImportFailure: ImportMismatchError('conftest', ...
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, ROOT_DIR)

from falcon import testing
from catcher.restapi import api
from catcher.models import User
import pytest


@pytest.fixture(scope='module')
def client():
    return testing.TestClient(api)


@pytest.fixture(scope='function')
def headers_with_admin_auth(session, users):
    user, api_key, valid_to = User.log_in(session, "admin_login", "admin_password")
    session.commit()
    return {'Content-Type': 'application/json', 'Authorization': api_key}


@pytest.fixture(scope='function')
def headers_with_user_auth(session, users):
    user, api_key, valid_to = User.log_in(session, "user1", "password1")
    session.commit()
    return {'Content-Type': 'application/json', 'Authorization': api_key}


@pytest.fixture(scope='session')
def headers():
    return {'Content-Type': 'application/json'}
